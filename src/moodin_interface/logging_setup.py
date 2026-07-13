"""Inisialisasi logging dari config/logging.yaml."""
from __future__ import annotations

import logging
import logging.config
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def setup_logging(level: str = "INFO") -> None:
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(exist_ok=True)

    cfg_path = PROJECT_ROOT / "config" / "logging.yaml"
    if cfg_path.exists():
        with cfg_path.open("r", encoding="utf-8") as fh:
            config = yaml.safe_load(fh)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level)

    logging.getLogger("moodin_interface").setLevel(level.upper())
