"""Klien MQTT (paho v2) yang mengonversi pesan menjadi sinyal Qt.

Berjalan di thread paho sendiri (loop_start). Emit sinyal Qt agar
konsumsi di thread GUI aman lewat koneksi queued default Qt.
"""
from __future__ import annotations

import logging

import paho.mqtt.client as mqtt
from PySide6.QtCore import QObject, Signal

from moodin_interface.config import MqttConfig
from moodin_interface.core.models import InferenceResult, PresenceEvent, SignalQuality
from moodin_interface.ipc.contracts import (
    Command,
    Topic,
    encode_command,
    parse_presence,
    parse_result,
    parse_signal_quality,
)

log = logging.getLogger(__name__)


class MqttClient(QObject):
    result_received = Signal(InferenceResult)
    signal_quality_received = Signal(SignalQuality)
    presence_received = Signal(PresenceEvent)
    connection_changed = Signal(bool)

    def __init__(self, cfg: MqttConfig) -> None:
        super().__init__()
        self._cfg = cfg
        self._client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=cfg.client_id,
        )
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_message = self._on_message

        if cfg.username:
            self._client.username_pw_set(cfg.username, cfg.password)
        if cfg.tls_ca:
            self._client.tls_set(ca_certs=cfg.tls_ca)

        self._client.reconnect_delay_set(
            min_delay=cfg.reconnect_min_delay,
            max_delay=cfg.reconnect_max_delay,
        )

    def start(self) -> None:
        log.info("Menghubungkan ke MQTT %s:%s", self._cfg.host, self._cfg.port)
        self._client.connect_async(self._cfg.host, self._cfg.port, self._cfg.keepalive)
        self._client.loop_start()

    def stop(self) -> None:
        self._client.loop_stop()
        self._client.disconnect()

    def publish_command(self, cmd: Command) -> None:
        self._client.publish(Topic.COMMAND.value, encode_command(cmd), qos=self._cfg.qos)
        log.debug("Publish perintah: %s", cmd.value)

    # ---------- Callback paho ----------
    def _on_connect(self, client, userdata, flags, reason_code, properties=None) -> None:
        if reason_code == 0:
            log.info("Terhubung ke broker MQTT")
            for topic in (Topic.INFERENCE_RESULT, Topic.SIGNAL_QUALITY, Topic.PRESENCE):
                client.subscribe(topic.value, qos=self._cfg.qos)
            self.connection_changed.emit(True)
        else:
            log.error("Gagal connect MQTT, reason=%s", reason_code)
            self.connection_changed.emit(False)

    def _on_disconnect(self, client, userdata, flags, reason_code, properties=None) -> None:
        log.warning("Terputus dari broker MQTT (reason=%s)", reason_code)
        self.connection_changed.emit(False)

    def _on_message(self, client, userdata, msg) -> None:
        try:
            if msg.topic == Topic.INFERENCE_RESULT.value:
                self.result_received.emit(parse_result(msg.payload))
            elif msg.topic == Topic.SIGNAL_QUALITY.value:
                self.signal_quality_received.emit(parse_signal_quality(msg.payload))
            elif msg.topic == Topic.PRESENCE.value:
                self.presence_received.emit(parse_presence(msg.payload))
        except (KeyError, ValueError) as exc:
            log.error("Payload tidak valid di %s: %s", msg.topic, exc)
