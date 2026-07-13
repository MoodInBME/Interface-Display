"""Loader konfigurasi: gabungkan app_config.yaml + variabel .env."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"


@dataclass(frozen=True)
class MqttConfig:
    host: str
    port: int
    username: str
    password: str
    tls_ca: str | None
    client_id: str
    keepalive: int
    qos: int
    reconnect_min_delay: int
    reconnect_max_delay: int


@dataclass(frozen=True)
class AppConfig:
    display_mode: str
    width: int
    height: int
    idle_timeout_seconds: int
    presence_grace_seconds: int
    db_path: str
    log_level: str
    mqtt: MqttConfig
    raw: dict[str, Any] = field(default_factory=dict)


def _read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def load_config() -> AppConfig:
    load_dotenv(PROJECT_ROOT / ".env")
    data = _read_yaml(CONFIG_DIR / "app_config.yaml")

    app = data.get("app", {})
    mqtt_yaml = data.get("mqtt", {})

    mqtt = MqttConfig(
        host=os.getenv("MOODIN_MQTT_HOST", "localhost"),
        port=int(os.getenv("MOODIN_MQTT_PORT", "8883")),
        username=os.getenv("MOODIN_MQTT_USERNAME", ""),
        password=os.getenv("MOODIN_MQTT_PASSWORD", ""),
        tls_ca=os.getenv("MOODIN_MQTT_TLS_CA") or None,
        client_id=os.getenv("MOODIN_MQTT_CLIENT_ID", "interface-display"),
        keepalive=int(mqtt_yaml.get("keepalive_seconds", 30)),
        qos=int(mqtt_yaml.get("qos", 1)),
        reconnect_min_delay=int(mqtt_yaml.get("reconnect_min_delay", 1)),
        reconnect_max_delay=int(mqtt_yaml.get("reconnect_max_delay", 30)),
    )

    return AppConfig(
        display_mode=os.getenv("MOODIN_DISPLAY_MODE", app.get("display_mode", "kiosk")),
        width=int(app.get("resolution", {}).get("width", 1024)),
        height=int(app.get("resolution", {}).get("height", 600)),
        idle_timeout_seconds=int(app.get("idle_timeout_seconds", 45)),
        presence_grace_seconds=int(app.get("presence_grace_seconds", 8)),
        db_path=os.getenv("MOODIN_DB_PATH", "data/moodin_ui.db"),
        log_level=os.getenv("MOODIN_LOG_LEVEL", "INFO"),
        mqtt=mqtt,
        raw=data,
    )
