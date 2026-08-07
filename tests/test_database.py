import os
import sqlite3
import pytest
from moodin_interface.data.database import TrendsDatabase

def test_migration_success(tmp_path):
    db_file = tmp_path / "test.db"
    conn = sqlite3.connect(db_file)
    conn.execute("""
        CREATE TABLE mood_log (
            id INTEGER PRIMARY KEY, session_id TEXT, mood_id TEXT, mood_label TEXT,
            confidence REAL, valence REAL, arousal REAL, heart_rate REAL, hrv_ms REAL, created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.execute("INSERT INTO mood_log (mood_id, mood_label, confidence, valence, arousal) VALUES ('ceria', 'Ceria', 0.9, 0.5, 0.5)")
    conn.execute("INSERT INTO mood_log (mood_id, mood_label, confidence, valence, arousal) VALUES ('3', 'Rileks', 0.9, -0.5, -0.5)")
    conn.commit()
    conn.close()
    
    db = TrendsDatabase(str(db_file))
    
    conn = sqlite3.connect(db_file)
    cur = conn.execute("SELECT typeof(mood_id), mood_id FROM mood_log ORDER BY id")
    rows = cur.fetchall()
    
    assert rows[0][0] == 'integer'
    assert rows[0][1] == 0
    
    assert rows[1][0] == 'integer'
    assert rows[1][1] == 3
    
    baks = list(tmp_path.glob("test.db.*.bak"))
    assert len(baks) == 1
    
    conn.close()
    db.close()

def test_migration_idempotent(tmp_path):
    db_file = tmp_path / "test.db"
    conn = sqlite3.connect(db_file)
    conn.execute("""
        CREATE TABLE mood_log (
            id INTEGER PRIMARY KEY, session_id TEXT, mood_id TEXT, mood_label TEXT,
            confidence REAL, valence REAL, arousal REAL, heart_rate REAL, hrv_ms REAL, created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.execute("INSERT INTO mood_log (mood_id, mood_label, confidence, valence, arousal) VALUES ('ceria', 'Ceria', 0.9, 0.5, 0.5)")
    conn.commit()
    conn.close()

    db = TrendsDatabase(str(db_file))
    db.close()
    
    baks = list(tmp_path.glob("test.db.*.bak"))
    assert len(baks) == 1
    for bak in baks:
        os.remove(bak)
        
    db2 = TrendsDatabase(str(db_file))
    baks2 = list(tmp_path.glob("test.db.*.bak"))
    
    assert len(baks2) == 0
    db2.close()

def test_migration_null_failure(tmp_path):
    db_file = tmp_path / "test.db"
    conn = sqlite3.connect(db_file)
    conn.execute("""
        CREATE TABLE mood_log (
            id INTEGER PRIMARY KEY, session_id TEXT, mood_id TEXT, mood_label TEXT,
            confidence REAL, valence REAL, arousal REAL, heart_rate REAL, hrv_ms REAL, created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.execute("INSERT INTO mood_log (mood_id, mood_label, confidence, valence, arousal) VALUES (NULL, 'Unknown', 0.9, -0.5, 0.5)")
    conn.commit()
    conn.close()
    
    with pytest.raises(ValueError, match="Ditemukan nilai mood_id tidak valid"):
        TrendsDatabase(str(db_file))
        
    conn = sqlite3.connect(db_file)
    cur = conn.execute("PRAGMA table_info(mood_log)")
    for col in cur.fetchall():
        if col[1] == 'mood_id':
            assert col[2].upper() == 'TEXT'
    conn.close()

def test_migration_missing_columns(tmp_path):
    db_file = tmp_path / "test.db"
    conn = sqlite3.connect(db_file)
    conn.execute("""
        CREATE TABLE mood_log (
            id INTEGER PRIMARY KEY, session_id TEXT, mood_id TEXT, mood_label TEXT,
            confidence REAL, valence REAL, arousal REAL, heart_rate REAL, created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()
    
    with pytest.raises(ValueError, match="Migrasi dibatalkan, kolom lama hilang: \\['hrv_ms'\\]"):
        TrendsDatabase(str(db_file))
