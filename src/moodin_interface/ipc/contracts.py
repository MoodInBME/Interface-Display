"""Kontrak IPC bersama antara 4 repo MoodIn. Ini adalah SATU-SATUNYA
sumber kebenaran untuk nama topik dan skema payload dari sisi UI.

Salin/duplikasi definisi topik ini ke Hardware-Connections dan
Software-Architecture agar payload konsisten (atau publish sebagai
package bersama di masa depan).
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from enum import Enum

from moodin_interface.core.models import InferenceResult, PresenceEvent, SignalQuality


class Topic(str, Enum):
    # Diterima UI (subscribe):
    INFERENCE_RESULT = "moodin/inference/result"
    SIGNAL_QUALITY = "moodin/signal/quality"
    PRESENCE = "moodin/presence"
    # Dipublish UI (perintah ke Hardware/Software):
    COMMAND = "moodin/ui/command"


class Command(str, Enum):
    START_CAPTURE = "start_capture"
    CANCEL_CAPTURE = "cancel_capture"


IPC_VERSION = "1.1.0"


def encode_command(cmd: Command) -> bytes:
    payload = {
        "command": cmd.value,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    return json.dumps(payload).encode("utf-8")


def parse_result(payload: bytes) -> InferenceResult:
    d = json.loads(payload)
    return InferenceResult(
        mood_id=_mood_id(d["mood_id"]),
        mood_label=str(d["mood_label"]),
        confidence=float(d["confidence"]),
        valence=float(d.get("valence", 0.0)),
        arousal=float(d.get("arousal", 0.0)),
        heart_rate_bpm=_opt_float(d.get("heart_rate_bpm")),
        hrv_ms=_opt_float(d.get("hrv_ms")),
        session_id=str(d.get("session_id", "")),
        physio_used=bool(d.get("physio_used", False)),
        simulated=bool(d.get("simulated", True)),
        version=str(d.get("version", "unknown")),
    )


def parse_signal_quality(payload: bytes) -> SignalQuality:
    d = json.loads(payload)
    return SignalQuality(
        quality=float(d["quality"]),
        face_detected=bool(d.get("face_detected", False)),
        illumination_ok=bool(d.get("illumination_ok", False)),
        message=str(d.get("message", "")),
    )


def parse_presence(payload: bytes) -> PresenceEvent:
    d = json.loads(payload)
    return PresenceEvent(
        present=bool(d["present"]),
        distance_cm=_opt_float(d.get("distance_cm")),
    )


_LEGACY_MOOD_IDS = {
    "ceria": 0, "cemas": 1, "tertekan": 2, "rileks": 3, "netral": 4,
}


def _mood_id(value: object) -> int:
    """Terima integer 0..4. String legacy diterima tapi diberi peringatan.

    Kontrak v1.1.0 menetapkan mood_id sebagai INTEGER. Penerjemahan string
    di sini hanya jaring pengaman selama Software-Architecture belum
    seragam; jangan dijadikan jalur normal.
    """
    if isinstance(value, bool):
        raise ValueError("mood_id tidak boleh boolean")
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        key = value.strip().lower()
        if key.isdigit():
            return int(key)
        if key in _LEGACY_MOOD_IDS:
            import logging
            logging.getLogger(__name__).warning(
                "mood_id string %r diterima; penerbit masih memakai "
                "kontrak lama. Harusnya integer 0..4.", value)
            return _LEGACY_MOOD_IDS[key]
    raise ValueError("mood_id tidak dikenal: " + repr(value))


def _opt_float(value: object) -> float | None:
    return float(value) if value is not None else None
