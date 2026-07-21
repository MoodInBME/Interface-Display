# Interface-Display
![https://img.shields.io/badge/github-repo-blue?logo=github](https://img.shields.io/badge/github-repo-blue?logo=github)

Lapisan antarmuka & tampilan (kiosk) untuk **MoodIn — Smart Mirror untuk Klasifikasi Mood Berbasis Graph Convolutional Network dan remote Photoplethysmography sebagai Personal Wellness Coach**.

Dibangun dengan **PySide6 + QML**, berjalan fullscreen di Raspberry Pi 5 (Debian Trixie) pada panel Waveshare 10.1" 1024x600. Repo ini adalah salah satu dari empat repo organisasi `MoodIn`:

| Repo                            | Peran                                                              |
| ------------------------------- | ------------------------------------------------------------------ |
| `MoodIn-master`               | Orkestrator / boot / intro alat                                    |
| `Hardware-Connections`        | Kamera, sensor, protokol fisik, presence                           |
| `Software-Architecture`       | Inferensi DL (ST-GCN + STC-rPPG), fusi VA-bridge                   |
| **`Interface-Display`** | **Layar kiosk: navigasi, input, tampilan hasil, tren lokal** |

## Arsitektur

```bash
    Hardware-Connections   Software-Architecture   Interface-Display (repo ini)
    (presence, sinyal)     (hasil inferensi)       (subscribe + publish command)
            \                     |                     /
             \                    |                    /
              +------------ MQTT Broker (TLS :8883) --+
```

`Interface-Display` **tidak melakukan inferensi**. Ia hanya:

1. Subscribe `moodin/inference/result`, `moodin/signal/quality`, `moodin/presence`.
2. Publish `moodin/ui/command` (mis. `start_capture`).
3. Menyimpan riwayat mood lokal (SQLite) untuk layar Tren 7 hari.

Lihat `docs/ipc-contract.md` untuk skema payload dan `docs/screen-map.md` untuk peta navigasi.

## Struktur folder

```bash
    Interface-Display/
    |-- config/          # app_config.yaml, logging.yaml (non-rahasia)
    |-- scripts/         # install.sh, run_kiosk.sh, systemd unit
    |-- src/moodin_interface/
    |   |-- app.py       # bootstrap QGuiApplication + QML engine
    |   |-- config.py    # loader konfigurasi (.env + yaml)
    |   |-- core/        # models, state_machine, bridge (Python<->QML)
    |   |-- ipc/         # contracts + mqtt_client
    |   |-- data/        # database.py (SQLite tren)
    |   `-- resources/qml/  # Main.qml + screens + components + theme
    |-- tests/
    `-- docs/
```

## Prasyarat

- Raspberry Pi 5 (16 GB) dengan Debian Trixie.
- Python 3.12 (bukan 3.14 — dukungan wheel PySide6/paho belum stabil).
- Broker MQTT aktif dengan TLS (sertifikat CA tersedia).
- Compositor Wayland (labwc/cage) atau eglfs untuk mode kiosk.

## Instalasi

```bash
    git clone https://github.com/MoodIn/Interface-Display.git /opt/moodin/Interface-Display
    cd /opt/moodin/Interface-Display
    bash scripts/install.sh
```

Skrip `install.sh` akan: memasang dependensi apt, membuat virtualenv, `pip install -e .`, menyalin `.env`, memasang systemd user service, dan mengaktifkan linger.

## Konfigurasi

1. Salin & edit environment:

```bash
        cp .env.example .env
        nano .env    # isi host broker, kredensial, path CA cert
```

2. Sesuaikan perilaku non-rahasia di `config/app_config.yaml` (resolusi, timeout idle, ambang mutu sinyal, kelas mood).

## Menjalankan

### Development (windowed, di desktop)

```bash
    source .venv/bin/activate
    MOODIN_DISPLAY_MODE=windowed python -m moodin_interface
```

### Produksi (kiosk, via systemd)

```bash
    systemctl --user start moodin-interface.service
    systemctl --user status moodin-interface.service
    journalctl --user -u moodin-interface.service -f
```

## Pengujian

```bash
    pip install -e ".[dev]"
    pytest
    ruff check src tests
```

## Integrasi dengan repo lain

- **Kontrak tunggal**: Semua nama topik & skema payload ada di `src/moodin_interface/ipc/contracts.py` dan didokumentasikan di `docs/ipc-contract.md`. Ketika `Software-Architecture` mengubah bentuk hasil inferensi, perbarui kontrak di kedua repo dan naikkan versi.
- **Urutan boot**: systemd unit di-set `After=moodin-hardware.service`. Sesuaikan bila nama service Hardware berbeda.
- **Tanpa import langsung**: UI tidak meng-import kode dari repo lain, hanya lewat MQTT. Ini menjaga empat repo tetap independen dan bisa di-deploy/versioning terpisah.

## Catatan privasi (UU PDP No. 27/2022)

MoodIn memproses data biometrik (wajah + rPPG) secara lokal di perangkat. Layar `OnboardingConsent` meminta persetujuan eksplisit sebelum akuisisi. Riwayat mood disimpan lokal di SQLite dan dapat dihapus pengguna.

## Lisensi

LGPL-3.0-or-later (mengikuti PySide6). Lihat `LICENSE`.

## Tim

VisionaryX 
Institut Teknologi Sepuluh Nopember
GEMASTIK Divisi 9 (Piranti Cerdas dan IoT).
