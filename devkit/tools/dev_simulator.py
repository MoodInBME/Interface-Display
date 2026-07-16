#!/usr/bin/env python3
"""Simulator lokal untuk menguji Interface-Display TANPA hardware.

Meniru repo Hardware-Connections + Software-Architecture dengan mem-publish
pesan MQTT ke broker lokal (localhost:1883, tanpa TLS).

Prasyarat: broker MQTT lokal berjalan, mis. Mosquitto:
    mosquitto -p 1883

Jalankan (dari root repo, venv aktif):
    python tools/dev_simulator.py

Alur: begitu UI mengirim 'start_capture', simulator membalas dengan mutu
sinyal menaik lalu satu hasil mood acak -> UI otomatis pindah ke ResultScreen.
"""
from __future__ import annotations

import json
import random
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883

TOPIC_RESULT = "moodin/inference/result"
TOPIC_QUALITY = "moodin/signal/quality"
TOPIC_PRESENCE = "moodin/presence"
TOPIC_COMMAND = "moodin/ui/command"

MOODS = [
    ("ceria", "Ceria", 0.7, 0.6),
    ("cemas", "Cemas", -0.5, 0.7),
    ("tertekan", "Tertekan", -0.6, -0.3),
    ("rileks", "Rileks", 0.5, -0.4),
    ("netral", "Netral", 0.0, 0.0),
]


def publish_result(client: mqtt.Client) -> None:
    mood_id, label, valence, arousal = random.choice(MOODS)
    payload = {
        "mood_id": mood_id,
        "mood_label": label,
        "confidence": round(random.uniform(0.70, 0.95), 2),
        "valence": valence,
        "arousal": arousal,
        "heart_rate_bpm": round(random.uniform(62, 88), 1),
        "hrv_ms": round(random.uniform(30, 60), 1),
        "session_id": datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S"),
    }
    client.publish(TOPIC_RESULT, json.dumps(payload), qos=1)
    print(f"[sim] hasil mood dipublikasikan: {label}")


def on_connect(client, userdata, flags, reason_code, properties=None) -> None:
    print(f"[sim] terhubung ke broker (rc={reason_code})")
    client.subscribe(TOPIC_COMMAND, qos=1)
    # Kirim presence=true (retained) agar IdleMirror bisa diklik.
    client.publish(
        TOPIC_PRESENCE,
        json.dumps({"present": True, "distance_cm": 40.0}),
        qos=1,
        retain=True,
    )
    print("[sim] presence=true dikirim. Klik layar cermin untuk masuk menu.")


def on_message(client, userdata, msg) -> None:
    try:
        data = json.loads(msg.payload)
    except ValueError:
        return
    if msg.topic == TOPIC_COMMAND and data.get("command") == "start_capture":
        print("[sim] menerima start_capture -> simulasi akuisisi ~3 dtk")
        for q in (0.4, 0.6, 0.85):
            client.publish(
                TOPIC_QUALITY,
                json.dumps({
                    "quality": q,
                    "face_detected": True,
                    "illumination_ok": True,
                    "message": "",
                }),
                qos=1,
            )
            time.sleep(1)
        publish_result(client)


def main() -> None:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="dev-simulator")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_HOST, BROKER_PORT, 30)
    print("[sim] simulator berjalan. Tekan Ctrl+C untuk berhenti.")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[sim] berhenti.")
        client.disconnect()


if __name__ == "__main__":
    main()
