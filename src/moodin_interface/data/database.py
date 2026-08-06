"""Penyimpanan lokal tren mood (SQLite). Sumber data TrendsScreen (7 hari)."""
from __future__ import annotations

import logging
import sqlite3
from pathlib import Path

from moodin_interface.core.models import InferenceResult

log = logging.getLogger(__name__)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS mood_log (
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
);
CREATE INDEX IF NOT EXISTS idx_mood_log_created ON mood_log(created_at);
"""


class TrendsDatabase:
    def __init__(self, db_path: str) -> None:
        path = Path(db_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()
        self._migrate_mood_id_to_int()

    def _migrate_mood_id_to_int(self) -> None:
        """Ubah baris lama yang menyimpan mood_id sebagai string.

        Basis data yang dibuat sebelum kontrak IPC v1.1.0 berisi nilai
        seperti "rileks". TrendsScreen memanggil Theme.moodColor() yang kini
        hanya menerima integer, sehingga baris lama akan tampil abu-abu
        tanpa pesan error. Konversi dilakukan sekali saat startup.
        """
        legacy = {
            "ceria": 0, "cemas": 1, "tertekan": 2,
            "rileks": 3, "netral": 4,
        }
        changed = 0
        for key, value in legacy.items():
            cur = self._conn.execute(
                "UPDATE mood_log SET mood_id = ? WHERE mood_id = ?",
                (value, key),
            )
            changed += cur.rowcount or 0
        if changed:
            self._conn.commit()
            log.info(
                "Migrasi mood_id string ke integer: %d baris.", changed)

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
