import json

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
    payload = json.dumps({
        "mood_id": "rileks",
        "mood_label": "Rileks",
        "confidence": 0.87,
        "valence": 0.6,
        "arousal": -0.3,
        "heart_rate_bpm": 72.5,
        "hrv_ms": 45.2,
        "session_id": "abc123",
    }).encode()
    r = parse_result(payload)
    assert r.mood_id == "rileks"
    assert r.confidence == 0.87
    assert r.heart_rate_bpm == 72.5


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
