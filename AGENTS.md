# AGENTS.md - Interface-Display (MoodIn)

> **ARSIP:** repo ini diarsipkan pada tahap Proposal Tugas Akhir (Pra-TA) dan tidak dikembangkan lagi. Instruksi di bawah adalah versi era GEMASTIK dan tidak berlaku untuk pekerjaan baru. Antarmuka baru dikembangkan di repo Interface-App.

Berlaku untuk seluruh isi repo ini. Dibaca otomatis oleh Antigravity CLI.

Versi 2. Versi 1 berisi struktur folder yang keliru; jangan dipakai lagi.

## 1. Apa yang dibangun

Antarmuka layar tertanam untuk MoodIn, smart mirror pengklasifikasi mood.
Aplikasi berjalan di Jetson Orin Nano Super, menampilkan hasil inferensi yang
dikirim repo `Software-Architecture` lewat MQTT.

Layar Waveshare 10.1 inci diputar ke **portrait 600x1024**. Semua tata letak
harus vertikal.

### Dua mode tampilan

`displayMode` adalah context property dari `app.py`. Nilainya **hanya** dua:

| Nilai | Kapan | Perilaku |
|-------|-------|----------|
| `kiosk` | di cermin, produksi | `Window.FullScreen`, font besar, sasaran sentuh 72 px |
| `windowed` | di laptop, pengembangan | `Window.Windowed`, font kecil, sasaran sentuh 48 px |

Jangan pernah menulis `displayMode === "mirror"` atau `=== "app"`. Nilai itu
tidak pernah ada. Perbandingannya akan selalu `false` tanpa error, dan cermin
diam-diam memakai ukuran font laptop. Gunakan `Theme.isMirror`.

## 2. Tumpukan teknologi

- Python 3.12, PySide6 (Qt 6), QML.
- `paho-mqtt` untuk IPC, SQLite untuk riwayat tren 7 hari.
- Tanpa kerangka web. Tanpa React, tanpa Tailwind, tanpa HTML.

## 3. Struktur direktori sebenarnya

`resources/` **tidak** berada di root repo. Letaknya di dalam paket Python.

    Interface-Display/
      AGENTS.md              <- berkas ini
      PROMPTS.md
      README.md
      pyproject.toml
      config/
        app_config.yaml      <- resolusi, timeout, kelas mood
        logging.yaml
      docs/
        ipc-contract.md      <- skema MQTT, v1.1.0
        screen-map.md        <- transisi antar layar
      scripts/
        install.sh  run_kiosk.sh  moodin-interface.service
      devkit/
        DEV_SETUP.md  tools/dev_simulator.py
      src/moodin_interface/
        app.py               <- entry point, addImportPath, context property
        config.py  logging_setup.py  __main__.py
        core/    bridge.py  models.py  state_machine.py
        data/    database.py
        ipc/     contracts.py  mqtt_client.py
        resources/qml/       <- SELURUH QML ADA DI SINI
          Main.qml
          theme/       Theme.qml  qmldir
          components/  PrimaryButton.qml  SignalBadge.qml
          screens/     SplashScreen.qml  IdleMirror.qml
                       OnboardingConsent.qml  MainMenu.qml
                       CaptureScreen.qml  ResultScreen.qml
                       TrendsScreen.qml  SettingsScreen.qml
      tests/     test_contracts.py  test_state_machine.py

Tidak ada direktori `ui/`. Tidak ada module QML bernama `MoodIn.Ui`.

`app.py` sudah memanggil `engine.addImportPath(str(QML_DIR))` dengan
`QML_DIR = .../resources/qml`. Jangan menambahkan import path lagi.

Impor di dalam QML memakai path relatif terhadap direktori itu:

    import "theme"
    import "components"
    import "screens" as Screens

`resources/qml/theme/qmldir` berisi `module theme` dan mendaftarkan `Theme`
sebagai singleton. Jangan membuat `qmldir` kedua di tempat lain.

## 4. Larangan keras

1. **Jangan membuat berkas baru di `screens/`.** Kedelapan layar sudah ada.
   25 frame Figma memetakan ke 8 layar itu; perbedaannya adalah keadaan, bukan
   berkas. Kecuali untuk kuesioner, lihat bagian 7.
2. **Jangan mengganti nama properti `Theme`.** Ada 79 rujukan `Theme.*` di
   kedelapan layar. Mengganti `fontBody` menjadi `fsBody` merusak semuanya
   dalam satu commit.
3. **Jangan menulis nilai heksadesimal langsung di layar.** Semua warna lewat
   `Theme`. Jika sebuah warna belum ada di `Theme`, berhenti dan tanyakan.
4. **Jangan memakai tema gelap.** Latar cermin adalah `#3A3A3A`. Palet
   `#0A0E12` / `#4FD1C5` pernah dipakai dan sudah ditolak tim.
5. **Jangan memanggil `get_variable_defs`.** File Figma MoodIn tidak
   mendefinisikan satu pun variable; hasilnya selalu `{}`. Gunakan
   `get_screenshot` dan `get_metadata`.
6. **Jangan memanggil `get_design_context`.** Keluarannya React + Tailwind dan
   tidak ada gunanya untuk QML.
7. **Jangan memakai `mood_id` bertipe string.** Kontrak v1.1.0 menetapkan
   integer 0..4.
8. **Jangan mengubah `state_machine.py` untuk menyiasati tata letak.** Berkas
   itu adalah sumber kebenaran alur layar.

## 5. Theme adalah sumber kebenaran

Berkas: `src/moodin_interface/resources/qml/theme/Theme.qml`, singleton.

Warna diambil dari pemindaian piksel 25 SVG hasil ekspor Figma, bukan dari
Figma Variables. Nama token lama dipertahankan seluruhnya. Ukuran font
bercabang lewat `Theme.isMirror`.

Warna mood diindeks integer dan urutannya wajib sama dengan `MOOD_CLASSES`
di `Software-Architecture/models/st_gcn_graph_tran/labels.py`:
0 Ceria, 1 Cemas, 2 Tertekan, 3 Rileks, 4 Netral.

## 6. Kontrak IPC v1.1.0

Baca `docs/ipc-contract.md`. Tiga hal yang wajib dihormati UI:

| Medan | Bila | UI harus |
|-------|------|----------|
| `simulated` | `true` | pita peringatan permanen, tidak bisa ditutup |
| `physio_used` | `false` | sembunyikan kartu TTV, jangan tampilkan angka lama |
| `confidence` | `< 0.5` | tanda ketidakpastian di samping label mood |

Menampilkan angka detak jantung hasil simulasi tanpa penanda adalah klaim
pengukuran yang tidak benar. Ini persoalan kejujuran, bukan sekadar gaya.

## 7. Pemetaan 25 frame Figma ke 8 layar

Nama layar berasal dari `core/state_machine.py`, bukan dari Figma.

| Layar QML | Frame Figma | Yang membedakan |
|-----------|-------------|-----------------|
| `SplashScreen.qml` | 02 | - |
| `IdleMirror.qml` | 01, 03, 16 | `bridge.userPresent`, `bridge.brokerConnected` |
| `OnboardingConsent.qml` | 09 | - |
| `MainMenu.qml` | 04, 11 | tamu vs terdaftar |
| `CaptureScreen.qml` | 10 | `bridge.signalQuality`, `qualityMessage` |
| `ResultScreen.qml` | 07, 14, 20, 23, 25, 24 | `bridge.moodId` lewat `Theme.moodColor()` |
| `TrendsScreen.qml` | 08, 15, 21 | rentang 7 hari vs harian |
| `SettingsScreen.qml` | 17, 05, 06, 13, 19 | subhalaman profil/avatar |

Lima frame hasil deteksi (07, 14, 20, 23, 25) adalah `ResultScreen` yang sama
dengan `mood_id` berbeda. Jangan membuat lima berkas.

**Frame 12, 18, 22 (kuesioner tiga langkah) belum punya state.** Ini kebutuhan
baru. Tambahkan state ke `state_machine.py` lebih dulu, berikut transisinya,
baru tulis QML-nya. Jangan mengarangnya sambil jalan.

## 8. Definisi selesai

Sebuah perubahan layar dianggap selesai bila:

1. `python -m moodin_interface` berjalan tanpa peringatan QML.
2. Tidak ada heksadesimal langsung; semua warna lewat `Theme`.
3. Terbaca pada 600x1024 tanpa scroll horizontal.
4. Diuji pada `MOODIN_DISPLAY_MODE=kiosk` dan `=windowed`.
5. `pytest` hijau.
6. Tidak ada berkas baru di `screens/` tanpa state yang bersesuaian.
7. Aturan degradasi bagian 6 dihormati.

## 9. Utang teknis yang diketahui

- `devkit/.env.dev` terlacak git dan memuat kunci MQTT. Periksa apakah isinya
  benar-benar placeholder.
- Branch repo ini `master`, sedangkan `Software-Architecture` memakai `main`.
- Rotasi portrait dilakukan di compositor, belum ada skrip otomatis.
- Basis data lama bisa memuat `mood_id` string; `database.py` memigrasikannya
  sekali saat startup.
