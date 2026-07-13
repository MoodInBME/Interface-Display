# Kontrak IPC MoodIn (v1)

Semua komunikasi antar-repo lewat MQTT broker (TLS, port 8883).
Sumber kebenaran kode: `src/moodin_interface/ipc/contracts.py`.

## Topik

| Topik | Arah | Publisher | Subscriber |
|-------|------|-----------|------------|
| `moodin/inference/result` | hasil mood | Software-Architecture | Interface-Display |
| `moodin/signal/quality`   | mutu sinyal rPPG | Hardware/Software | Interface-Display |
| `moodin/presence`         | kehadiran user | Hardware-Connections | Interface-Display |
| `moodin/ui/command`       | perintah UI | Interface-Display | Hardware/Software |

## Skema payload (JSON)

### moodin/inference/result

    {
      "mood_id": "rileks",
      "mood_label": "Rileks",
      "confidence": 0.87,
      "valence": 0.6,
      "arousal": -0.3,
      "heart_rate_bpm": 72.5,
      "hrv_ms": 45.2,
      "session_id": "abc123"
    }

`mood_id` wajib salah satu dari: `ceria`, `cemas`, `tertekan`, `rileks`, `netral`.

### moodin/signal/quality

    { "quality": 0.72, "face_detected": true, "illumination_ok": true, "message": "" }

### moodin/presence

    { "present": true, "distance_cm": 35.0 }

### moodin/ui/command

    { "command": "start_capture", "ts": "2026-07-13T07:14:00Z" }

`command` salah satu dari: `start_capture`, `cancel_capture`.

## Versi & kompatibilitas

Perubahan skema harus menaikkan versi dokumen ini dan disepakati oleh
ketiga repo lain sebelum di-deploy.
