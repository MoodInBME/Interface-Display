#!/usr/bin/env bash
# Launcher kiosk fullscreen untuk MoodIn Interface-Display.
set -euo pipefail

APP_HOME="/opt/moodin/Interface-Display"
cd "${APP_HOME}"

# shellcheck disable=SC1091
source .venv/bin/activate

# Platform Qt: utamakan Wayland (labwc/wayfire), fallback eglfs jika headless compositor.
export QT_QPA_PLATFORM="${QT_QPA_PLATFORM:-wayland;eglfs}"
export QT_QPA_EGLFS_INTEGRATION="${QT_QPA_EGLFS_INTEGRATION:-eglfs_kms}"

# Sembunyikan kursor mouse pada kiosk sentuh.
export QT_QPA_EGLFS_HIDECURSOR=1

# Paksa skala 1x pada panel 1024x600.
export QT_SCALE_FACTOR=1

# Muat variabel dari .env bila ada.
if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

exec python -m moodin_interface
