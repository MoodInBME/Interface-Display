# Inisialisasi Interface-Display di Laptop (Development)

Panduan ini untuk menjalankan UI di laptop (Windows/macOS/Linux) dalam mode
*windowed*. **Jangan** jalankan `scripts/install.sh` atau `scripts/run_kiosk.sh`
di laptop — keduanya khusus Raspberry Pi (apt, systemd, Wayland/eglfs).

## 0. Yang perlu dipasang

- **Python 3.12** (bukan 3.13/3.14 — wheel PySide6 6.7.2 belum tersedia untuk versi terbaru).
- **Git**.
- **PySide6 sudah membawa runtime Qt + QML sendiri** — tidak perlu instal Qt terpisah.
- (Opsional) **Mosquitto** sebagai broker MQTT lokal untuk menguji navigasi penuh.

## 1. Ambil kode

```bash
git clone https://github.com/MoodInBME/Interface-Display.git
cd Interface-Display
```

Jika repo GitHub masih kosong, ekstrak isi ZIP ke folder lalu:

```bash
git init
git add .
git commit -m "chore: inisialisasi Interface-Display"
git branch -M main
git remote add origin https://github.com/MoodInBME/Interface-Display.git
git push -u origin main
```

## 2. Buat & aktifkan virtual environment

**Windows (PowerShell):**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

## 3. Instal dependensi

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

Ini memasang: PySide6, paho-mqtt, PyYAML, python-dotenv (+ pytest, ruff untuk dev).

## 4. Siapkan environment lokal

Salin `.env.dev` menjadi `.env` (mengarah ke broker lokal tanpa TLS, mode windowed):

```bash
cp .env.dev .env      # Windows: copy .env.dev .env
```

## 5. Jalankan

```bash
python -m moodin_interface
```

Yang terjadi:

- Muncul jendela **Splash** -> otomatis ke **IdleMirror** setelah 2,5 detik.
- Tanpa broker, status broker = *Terputus* dan **layar cermin tidak bisa diklik**
  (menunggu sinyal presence). Ini normal. Lanjut ke langkah 6 untuk navigasi penuh.

## 6. (Opsional) Uji navigasi penuh dengan broker + simulator

UI baru bisa masuk ke menu setelah menerima `presence=true`, dan tombol
"Deteksi Mood" aktif hanya saat broker terhubung. Jalankan broker + simulator:

**Terminal A — broker:**

```bash
mosquitto -p 1883
```

Instal Mosquitto bila belum ada:

- Windows: unduh installer dari mosquitto.org, atau `winget install EclipseMosquitto.Mosquitto`
- macOS: `brew install mosquitto`
- Linux (Debian/Ubuntu): `sudo apt install mosquitto mosquitto-clients`

**Terminal B — UI:**

```bash
source .venv/bin/activate
python -m moodin_interface
```

**Terminal C — simulator (venv aktif):**

```bash
python tools/dev_simulator.py
```

Alur uji: simulator kirim `presence=true` -> klik layar cermin -> **Menu Utama**
-> "Deteksi Mood" -> simulator membalas mutu sinyal + hasil mood acak ->
UI pindah ke **ResultScreen** -> "Lihat Tren" menampilkan data dari SQLite.

## 7. Menjalankan tes

```bash
pytest
ruff check src tests
```

## Ekstensi editor yang disarankan (VS Code)

- **Python** (ms-python.python) + **Pylance**
- **Ruff** (charliermarsh.ruff) — linting/format
- **Qt for Python** atau **QML** — syntax highlighting file `.qml`

## Masalah umum

- `ModuleNotFoundError: moodin_interface` -> pastikan `pip install -e .` sudah
  dijalankan dan venv aktif.
- Jendela tidak muncul / error platform Qt di Linux -> pasang `libxcb` dkk, atau
  set `QT_QPA_PLATFORM=xcb`. Di laptop biasanya tidak perlu.
- PySide6 gagal instal -> cek `python --version` benar 3.12.
- QML tidak ketemu modul `theme` -> jalankan lewat `python -m moodin_interface`
  (bukan menjalankan `app.py` langsung), karena import path di-set di sana.
