"""Penyimpanan lokal tren mood (SQLite). Sumber data TrendsScreen (7 hari)."""
from __future__ import annotations

import logging
import sqlite3
from datetime import datetime
from pathlib import Path

from moodin_interface.core.models import InferenceResult

log = logging.getLogger(__name__)

_MOOD_LOG_COLUMNS_SQL = """
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id   TEXT,
    mood_id      INTEGER NOT NULL,
    mood_label   TEXT NOT NULL,
    confidence   REAL NOT NULL,
    valence      REAL NOT NULL,
    arousal      REAL NOT NULL,
    heart_rate   REAL,
    hrv_ms       REAL,
    created_at   TEXT NOT NULL DEFAULT (datetime('now'))
"""

_REQUIRED_COLS = [
    line.strip().split()[0]
    for line in _MOOD_LOG_COLUMNS_SQL.strip().split("\n")
    if line.strip()
]

_SCHEMA = f"""
CREATE TABLE IF NOT EXISTS mood_log (
{_MOOD_LOG_COLUMNS_SQL}
);
CREATE INDEX IF NOT EXISTS idx_mood_log_created ON mood_log(created_at);
"""


class TrendsDatabase:
    def __init__(self, db_path: str) -> None:
        path = Path(db_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self._db_path = path
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()
        self._migrate_mood_id_to_int()

    def _migrate_mood_id_to_int(self) -> None:
        cur = self._conn.execute("PRAGMA table_info(mood_log)")
        columns = cur.fetchall()
        
        needs_migration = False
        col_names = []
        for col in columns:
            col_names.append(col["name"])
            if col["name"] == "mood_id" and col["type"].upper() != "INTEGER":
                needs_migration = True
                
        if not needs_migration:
            return
            
        log.info("Memulai migrasi skema mood_log...")
        
        missing_cols = [c for c in _REQUIRED_COLS if c not in col_names]
        if missing_cols:
            msg = f"Migrasi dibatalkan, kolom lama hilang: {missing_cols}"
            log.error(msg)
            raise ValueError(msg)
            
        if self._conn.in_transaction:
            self._conn.commit()
            
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        base_bak_path = str(self._db_path) + f".{ts}.bak"
        bak_path = base_bak_path
        counter = 1
        while Path(bak_path).exists():
            bak_path = f"{base_bak_path}.{counter}"
            counter += 1
            
        self._conn.execute(f"VACUUM INTO '{bak_path}'")
        log.info("Backup database disimpan di %s", bak_path)
        
        self._conn.execute("BEGIN TRANSACTION")
            
        try:
            legacy = {
                "ceria": 0, "cemas": 1, "tertekan": 2,
                "rileks": 3, "netral": 4,
            }
            for key, value in legacy.items():
                self._conn.execute(
                    "UPDATE mood_log SET mood_id = ? WHERE mood_id = ?",
                    (value, key),
                )
                
            cur = self._conn.execute(
                """
                SELECT rowid, typeof(mood_id) as t, mood_id 
                FROM mood_log 
                WHERE NOT (
                    (typeof(mood_id) = 'integer' AND mood_id IN (0, 1, 2, 3, 4))
                    OR 
                    (typeof(mood_id) = 'text' AND mood_id GLOB '[0-4]')
                )
                """
            )
            bad_rows = cur.fetchall()
            if bad_rows:
                bad_info = [f"rowid {r[0]}: {r[1]} ({r[2]})" for r in bad_rows]
                msg = f"Ditemukan nilai mood_id tidak valid: {bad_info}"
                log.error(msg)
                raise ValueError(msg)
                
            cur = self._conn.execute("PRAGMA index_list(mood_log)")
            index_sqls = []
            for idx in cur.fetchall():
                if not idx["name"].startswith("sqlite_autoindex"):
                    cur_idx = self._conn.execute("SELECT sql FROM sqlite_master WHERE type='index' AND name=?", (idx["name"],))
                    idx_sql = cur_idx.fetchone()
                    if idx_sql and idx_sql["sql"]:
                        index_sqls.append(idx_sql["sql"])
            
            self._conn.execute(f"""
                CREATE TABLE mood_log_new (
{_MOOD_LOG_COLUMNS_SQL}
                )
            """)
            
            cur = self._conn.execute("""
                INSERT INTO mood_log_new 
                SELECT id, session_id, CAST(mood_id AS INTEGER), mood_label, confidence, valence, arousal, heart_rate, hrv_ms, COALESCE(created_at, datetime('now'))
                FROM mood_log
            """)
            rows_copied = cur.rowcount
            
            self._conn.execute("DROP TABLE mood_log")
            self._conn.execute("ALTER TABLE mood_log_new RENAME TO mood_log")
            
            for sql in index_sqls:
                self._conn.execute(sql)
                
            self._conn.commit()
            log.info("Migrasi skema selesai. %d baris dipindahkan.", rows_copied)
            
        except Exception as e:
            self._conn.rollback()
            log.error("Migrasi gagal: %s", e)
            raise

    def insert_result(self, r: InferenceResult) -> None:
        self._conn.execute(
            """
            INSERT INTO mood_log
                (session_id, mood_id, mood_label, confidence, valence, arousal, heart_rate, hrv_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                r.session_id, r.mood_id, r.mood_label, r.confidence,
                r.valence, r.arousal, r.heart_rate_bpm, r.hrv_ms,
            ),
        )
        self._conn.commit()

    def recent_moods(self, days: int = 7) -> list[dict]:
        cur = self._conn.execute(
            """
            SELECT mood_id, mood_label, confidence, heart_rate, created_at
            FROM mood_log
            WHERE datetime(created_at) >= datetime('now', ?)
            ORDER BY datetime(created_at) DESC
            """,
            (f"-{int(days)} days",),
        )
        return [dict(row) for row in cur.fetchall()]

    def close(self) -> None:
        self._conn.close()
