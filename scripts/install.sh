#!/usr/bin/env bash
# Instalasi Interface-Display di Jetson Orin Nano Super (Ubuntu 24.04).
# Jalankan sebagai user 'moodin' (bukan root), kecuali langkah apt.
set -euo pipefail

APP_USER="${APP_USER:-moodin}"
APP_HOME="/opt/moodin/Interface-Display"
PYTHON_BIN="${PYTHON_BIN:-python3.12}"

echo "[1/6] Instalasi dependensi sistem (butuh sudo)..."
sudo apt-get update
sudo apt-get install -y \
  "${PYTHON_BIN}" "${PYTHON_BIN}-venv" \
  libgl1 libegl1 libxkbcommon0 libdbus-1-3 \
  fonts-inter

echo "[2/6] Membuat virtualenv..."
cd "${APP_HOME}"
"${PYTHON_BIN}" -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate

echo "[3/6] Upgrade pip & install project..."
pip install --upgrade pip wheel
pip install -e .

echo "[4/6] Menyiapkan .env & folder runtime..."
[ -f .env ] || cp .env.example .env
mkdir -p data logs

echo "[5/6] Memasang systemd user service..."
mkdir -p "${HOME}/.config/systemd/user"
cp scripts/moodin-interface.service "${HOME}/.config/systemd/user/"
systemctl --user daemon-reload
systemctl --user enable moodin-interface.service

echo "[6/6] Mengaktifkan linger agar service jalan tanpa login..."
sudo loginctl enable-linger "${APP_USER}"

echo "Selesai. Edit .env lalu jalankan: systemctl --user start moodin-interface.service"
