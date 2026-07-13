"""Jembatan Python <-> QML. Semua state UI diekspos lewat properti Qt."""
from __future__ import annotations

import logging

from PySide6.QtCore import Property, QObject, Signal, Slot

from moodin_interface.core.models import InferenceResult, PresenceEvent, SignalQuality
from moodin_interface.core.state_machine import Screen, StateMachine
from moodin_interface.data.database import TrendsDatabase
from moodin_interface.ipc.contracts import Command
from moodin_interface.ipc.mqtt_client import MqttClient

log = logging.getLogger(__name__)


class UiBridge(QObject):
    """Objek konteks tunggal yang di-bind ke root QML sebagai `bridge`."""

    # --- Sinyal ke QML ---
    screenChanged = Signal()
    resultChanged = Signal()
    signalQualityChanged = Signal()
    presenceChanged = Signal()
    connectionChanged = Signal()

    def __init__(self, mqtt: MqttClient, db: TrendsDatabase) -> None:
        super().__init__()
        self._sm = StateMachine(Screen.SPLASH)
        self._mqtt = mqtt
        self._db = db

        self._mood_label = ""
        self._mood_id = ""
        self._confidence = 0.0
        self._heart_rate = 0.0
        self._signal_quality = 0.0
        self._quality_message = ""
        self._present = False
        self._connected = False

        # Hubungkan sinyal MQTT ke handler bridge.
        self._mqtt.result_received.connect(self._on_result)
        self._mqtt.signal_quality_received.connect(self._on_signal_quality)
        self._mqtt.presence_received.connect(self._on_presence)
        self._mqtt.connection_changed.connect(self._on_connection)

    # ---------- Properti terekspos ke QML ----------
    @Property(str, notify=screenChanged)
    def currentScreen(self) -> str:
        return self._sm.current.value

    @Property(str, notify=resultChanged)
    def moodLabel(self) -> str:
        return self._mood_label

    @Property(str, notify=resultChanged)
    def moodId(self) -> str:
        return self._mood_id

    @Property(float, notify=resultChanged)
    def confidence(self) -> float:
        return self._confidence

    @Property(float, notify=resultChanged)
    def heartRate(self) -> float:
        return self._heart_rate

    @Property(float, notify=signalQualityChanged)
    def signalQuality(self) -> float:
        return self._signal_quality

    @Property(str, notify=signalQualityChanged)
    def qualityMessage(self) -> str:
        return self._quality_message

    @Property(bool, notify=presenceChanged)
    def userPresent(self) -> bool:
        return self._present

    @Property(bool, notify=connectionChanged)
    def brokerConnected(self) -> bool:
        return self._connected

    # ---------- Slot dipanggil dari QML ----------
    @Slot(str)
    def navigate(self, target_value: str) -> None:
        try:
            target = Screen(target_value)
        except ValueError:
            log.warning("Target layar tidak dikenal: %s", target_value)
            return
        if self._sm.transition(target):
            self.screenChanged.emit()
        else:
            log.warning("Transisi ilegal: %s -> %s", self._sm.current.value, target_value)

    @Slot()
    def startCapture(self) -> None:
        """Minta layer Hardware/Software mulai akuisisi + inferensi."""
        self._mqtt.publish_command(Command.START_CAPTURE)
        self.navigate(Screen.CAPTURE.value)

    @Slot()
    def cancelCapture(self) -> None:
        self._mqtt.publish_command(Command.CANCEL_CAPTURE)
        self.navigate(Screen.MAIN_MENU.value)

    @Slot(result="QVariantList")
    def loadTrends(self) -> list[dict]:
        """Ambil 7 hari terakhir untuk TrendsScreen."""
        return self._db.recent_moods(days=7)

    # ---------- Handler dari MQTT ----------
    def _on_result(self, result: InferenceResult) -> None:
        self._mood_id = result.mood_id
        self._mood_label = result.mood_label
        self._confidence = result.confidence
        self._heart_rate = result.heart_rate_bpm or 0.0
        self._db.insert_result(result)
        self.resultChanged.emit()
        self.navigate(Screen.RESULT.value)

    def _on_signal_quality(self, sq: SignalQuality) -> None:
        self._signal_quality = sq.quality
        self._quality_message = sq.message
        self.signalQualityChanged.emit()

    def _on_presence(self, ev: PresenceEvent) -> None:
        self._present = ev.present
        self.presenceChanged.emit()

    def _on_connection(self, connected: bool) -> None:
        self._connected = connected
        self.connectionChanged.emit()
