import json

import pytest

import pytest

from moodin_interface.ipc.contracts import (
    Command,
    encode_command,
    parse_presence,
    parse_result,
    parse_signal_quality,
)

def test_encode_command_roundtrip():
    raw = encode_command(Command.START_CAPTURE)
    payload = json.loads(raw)
    assert payload["command"] == "start_capture"
    assert "ts" in payload


def test_parse_result_full():
    # Kontrak v1.1.0: mood_id adalah integer 0..4.
    payload = json.dumps({
        "mood_id": 3,
        "mood_label": "Rileks",
        "confidence": 0.87,
        "valence": 0.6,
        "arousal": -0.3,
        "heart_rate_bpm": 72.5,
        "hrv_ms": 45.2,
        "physio_used": True,
        "simulated": False,
        "session_id": "abc123",
        "version": "1.1.0",
    }).encode()
    r = parse_result(payload)
    assert r.mood_id == 3
    assert isinstance(r.mood_id, int)
    assert r.confidence == 0.87
    assert r.heart_rate_bpm == 72.5
    assert r.physio_used is True
    assert r.simulated is False


def test_parse_result_defaults_are_conservative():
    # Tanpa medan baru, UI harus menganggap TTV tidak dipakai.
    payload = json.dumps({
        "mood_id": 0,
        "mood_label": "Ceria",
        "confidence": 0.5,
    }).encode()
    r = parse_result(payload)
    assert r.physio_used is False
    assert r.simulated is False


def test_parse_result_accepts_legacy_string_with_warning(caplog):
    # String legacy diterjemahkan, tetapi harus tercatat sebagai peringatan.
    payload = json.dumps({
        "mood_id": "rileks",
        "mood_label": "Rileks",
        "confidence": 0.7,
    }).encode()
    with caplog.at_level("WARNING"):
        r = parse_result(payload)
    assert r.mood_id == 3
    assert any("kontrak lama" in rec.message for rec in caplog.records)


def test_parse_result_rejects_unknown_mood():
    payload = json.dumps({
        "mood_id": "bahagia_sekali",
        "mood_label": "?",
        "confidence": 0.7,
    }).encode()
    with pytest.raises(ValueError):
        parse_result(payload)


def test_parse_result_rejects_out_of_range():
    payload = json.dumps({
        "mood_id": 9,
        "mood_label": "?",
        "confidence": 0.7,
    }).encode()
    with pytest.raises(ValueError):
        parse_result(payload)


def test_parse_signal_quality_defaults():
    payload = json.dumps({"quality": 0.4}).encode()
    sq = parse_signal_quality(payload)
    assert sq.quality == 0.4
    assert sq.face_detected is False


def test_parse_presence():
    payload = json.dumps({"present": True, "distance_cm": 35.0}).encode()
    ev = parse_presence(payload)
    assert ev.present is True
    assert ev.distance_cm == 35.0
