"""Model data domain UI (independen dari transport)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class InferenceResult:
    """Hasil klasifikasi mood dari repo Software-Architecture."""
    mood_id: str                 # ceria | cemas | tertekan | rileks | netral
    mood_label: str
    confidence: float            # 0..1
    valence: float               # -1..1
    arousal: float               # -1..1
    heart_rate_bpm: float | None
    hrv_ms: float | None
    session_id: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class SignalQuality:
    """Mutu sinyal rPPG saat capture (dari Hardware/Software layer)."""
    quality: float               # 0..1
    face_detected: bool
    illumination_ok: bool
    message: str = ""


@dataclass(frozen=True)
class PresenceEvent:
    """Deteksi kehadiran user di depan cermin."""
    present: bool
    distance_cm: float | None = None
