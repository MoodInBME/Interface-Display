# Interface-Display
![https://img.shields.io/badge/github-repo-blue?logo=github](https://img.shields.io/badge/github-repo-blue?logo=github)

Lapisan antarmuka & tampilan (kiosk) untuk **MoodIn — Smart Mirror untuk Klasifikasi Mood Berbasis Graph Convolutional Network dan remote Photoplethysmography sebagai Personal Wellness Coach**.

Dibangun dengan **PySide6 + QML**, berjalan fullscreen pada panel Waveshare 10.1" 1024x600. Target utama saat ini **NVIDIA Jetson Orin Nano Super (8 GB, Ubuntu 24.04, JetPack 7.2)** — board yang sama dengan mesin inferensi. Repo ini adalah salah satu dari empat repo organisasi `MoodIn`:

| Repo | Peran |
| --- | --- |
| `MoodIn-master` | Orkestrator / boot / intro alat |
| `Hardware-Connections` | Kamera, sensor, protokol fisik, presence |
| `Software-Architecture` | Inferensi DL (ST-GCN + STC-rPPG), fusi VA-bridge |
| **`Interface-Display`** | **Layar kiosk: navigasi, input, tampilan hasil, tren lokal** |

## Arsitektur & Peran
Repo ini **tidak memuat model dan tidak melakukan inferensi**. Ia hanya berlangganan MQTT dan menggambar layar berdasarkan kontrak *payload*.
```
    Hardware-Connections   Software-Architecture   Interface-Display (repo ini)
    (presence, sinyal)     (hasil inferensi)       (subscribe + publish command)
            \                     |                     /
             \                    |                    /
              +------------ MQTT Broker (TLS :8883) --+
```

## 1. Anda tidak perlu menunggu model
Seluruh UI dapat dikembangkan dan diuji mandiri hari ini, tanpa Jetson, tanpa kamera, tanpa checkpoint. 
Anda dapat menggunakan `mock_inference_publisher.py` (yang dapat di-generate dari `Software-Architecture`) untuk mengirim *payload* *dummy* via MQTT.

Skenario *mock* yang didukung:
| `--scenario` | Perilaku | Menguji |
|---|---|---|
| `cycle` | berputar melewati kelima mood | transisi kartu, animasi, warna |
| `stable` | satu mood tetap | layar diam, keterbacaan jangka panjang |
| `degraded` | `physio_used=false`, SNR rendah | jalur degradasi, kartu TTV tersembunyi |
| `noisy` | VA acak | ketahanan terhadap kedip dan lonjakan |

## 2. Aturan Degradasi (Spesifikasi UI Wajib)

| Kondisi | Perilaku UI yang wajib |
|---|---|
| `physio_used=false` | Tampilkan mood, **sembunyikan** kartu tanda vital. Jangan tampilkan HR terakhir yang basi. |
| `face_detected=false` (>3s)| Kembali ke layar idle. |
| `buffer_fill < 1.0` | Tampilkan progress ring. Jangan pernah menampilkan mood dari jendela yang belum penuh. |
| `presence=offline` | Banner engine terputus, bekukan kartu, redupkan. |
| `confidence < 0.5` | Tampilkan mood dengan penanda ketidakpastian, jangan menyembunyikannya. |

*Prinsip: Menampilkan angka basi pada perangkat kesehatan lebih buruk daripada tidak menampilkan apa pun.*

## 3. Desain Layar (Dua Permukaan)
**Cermin (Layar 10,1 inci 1024x600 landscape).** Dilihat dari jarak sekitar 55 cm di balik kaca dua arah (absorpsi 80-90% cahaya).
- Latar **hitam pekat**. Setiap piksel terang membuang anggaran cahaya yang sudah tipis.
- Kontras tinggi, ukuran font minimum besar. Tanpa hover/elemen sentuh presisi. Animasi harus halus dan lambat.

**Aplikasi Pendamping (Android/iOS).** Menangani autentikasi, pendaftaran, dan melihat riwayat data secara penuh. Cermin tetap dapat beroperasi dalam **mode tamu** tanpa login/riwayat.

## 4. Struktur Folder & Modul

```
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
`-- docs/            # ipc-contract.md, screen-map.md, figma-links.md
```

## 5. Prasyarat & Instalasi
- **NVIDIA Jetson Orin Nano Super** (Ubuntu 24.04, JetPack 7.2).
- Panel Waveshare masuk lewat HDMI; gunakan adapter aktif **DP→HDMI** untuk Jetson.
- Broker MQTT aktif dengan TLS (sertifikat CA tersedia).

```bash
git clone https://github.com/MoodInBME/Interface-Display.git /opt/moodin/Interface-Display
cd /opt/moodin/Interface-Display
bash scripts/install.sh
```

### Development (windowed)
```bash
source .venv/bin/activate
MOODIN_DISPLAY_MODE=windowed python -m moodin_interface
```

## 6. Privasi di sisi UI (UU PDP No. 27/2022)
UI **tidak pernah** menerima citra wajah maupun landmark mentah dari MQTT. Pengenalan wajah diproses murni di perangkat *edge*; yang menyeberang ke MQTT hanyalah skalar numerik. Data riwayat disimpan secara lokal di SQLite dan dapat dihapus.

## Lisensi & Tim
- LGPL-3.0-or-later (mengikuti PySide6). Lihat `LICENSE`.
- **VisionaryX** - Institut Teknologi Sepuluh Nopember (GEMASTIK Divisi 9)
