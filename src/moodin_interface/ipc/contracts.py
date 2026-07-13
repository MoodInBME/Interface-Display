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


def encode_command(cmd: Command) -> bytes:
    payload = {
        "command": cmd.value,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    return json.dumps(payload).encode("utf-8")


def parse_result(payload: bytes) -> InferenceResult:
    d = json.loads(payload)
    return InferenceResult(
        mood_id=str(d["mood_id"]),
        mood_label=str(d["mood_label"]),
        confidence=float(d["confidence"]),
        valence=float(d.get("valence", 0.0)),
        arousal=float(d.get("arousal", 0.0)),
        heart_rate_bpm=_opt_float(d.get("heart_rate_bpm")),
        hrv_ms=_opt_float(d.get("hrv_ms")),
        session_id=str(d.get("session_id", "")),
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


def _opt_float(value: object) -> float | None:
    return float(value) if value is not None else None
