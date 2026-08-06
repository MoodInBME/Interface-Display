"""Model data domain UI (independen dari transport)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

# Urutan WAJIB sama dengan MOOD_CLASSES di
# Software-Architecture/models/st_gcn_graph_tran/labels.py
MOOD_CLASSES = ("Ceria", "Cemas", "Tertekan", "Rileks", "Netral")


def mood_label_for(mood_id: int) -> str:
    """Label manusiawi untuk mood_id 0..4."""
    if 0 <= mood_id < len(MOOD_CLASSES):
        return MOOD_CLASSES[mood_id]
    return "Tidak diketahui"


@dataclass(frozen=True)
class InferenceResult:
    """Hasil klasifikasi mood dari repo Software-Architecture.

    mood_id adalah INTEGER 0..4, bukan string. Penerbitnya adalah
    Software-Architecture, dan labels.py di sana yang menentukan urutannya:
    0 Ceria, 1 Cemas, 2 Tertekan, 3 Rileks, 4 Netral.
    """

    mood_id: int                 # 0..4
    mood_label: str
    confidence: float            # 0..1
    valence: float               # -1..1
    arousal: float               # -1..1
    heart_rate_bpm: float | None
    hrv_ms: float | None
    session_id: str = ""
    physio_used: bool = False    # False -> sembunyikan kartu TTV
    simulated: bool = False      # True  -> tampilkan pita MODE DEMO
    version: str = "1.1.0"
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if not isinstance(self.mood_id, int) or not 0 <= self.mood_id <= 4:
            raise ValueError(
                "mood_id harus integer 0..4, diterima: " + repr(self.mood_id))


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
