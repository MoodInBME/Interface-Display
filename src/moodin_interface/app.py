"""Bootstrap aplikasi: QGuiApplication + QQmlApplicationEngine + bridge."""
from __future__ import annotations

import logging
import signal
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

from moodin_interface.config import load_config
from moodin_interface.core.bridge import UiBridge
from moodin_interface.data.database import TrendsDatabase
from moodin_interface.ipc.mqtt_client import MqttClient
from moodin_interface.logging_setup import setup_logging

log = logging.getLogger(__name__)

QML_DIR = Path(__file__).resolve().parent / "resources" / "qml"
QML_ROOT = QML_DIR / "Main.qml"


def run(argv: list[str]) -> int:
    cfg = load_config()
    setup_logging(cfg.log_level)
    log.info("Memulai MoodIn Interface-Display (mode=%s)", cfg.display_mode)

    QQuickStyle.setStyle("Basic")
    app = QGuiApplication(argv)

    db = TrendsDatabase(cfg.db_path)
    mqtt = MqttClient(cfg.mqtt)
    mqtt.setParent(app)
    bridge = UiBridge(mqtt, db)
    bridge.setParent(app)

    engine = QQmlApplicationEngine()
    # Tambahkan folder qml sebagai import path agar modul 'theme' bisa di-resolve.
    engine.addImportPath(str(QML_DIR))

    ctx = engine.rootContext()
    ctx.setContextProperty("bridge", bridge)
    ctx.setContextProperty("appWidth", cfg.width)
    ctx.setContextProperty("appHeight", cfg.height)
    ctx.setContextProperty("displayMode", cfg.display_mode)

    engine.load(QUrl.fromLocalFile(str(QML_ROOT)))
    if not engine.rootObjects():
        log.error("Gagal memuat Main.qml")
        return 1

    mqtt.start()

    # Tangani SIGINT/SIGTERM agar systemd bisa stop bersih.
    signal.signal(signal.SIGINT, lambda *_: app.quit())
    signal.signal(signal.SIGTERM, lambda *_: app.quit())

    exit_code = app.exec()

    del engine

    mqtt.stop()
    db.close()
    logger.info(f"Aplikasi berhenti (exit_code={exit_code})")
    return exit_code
