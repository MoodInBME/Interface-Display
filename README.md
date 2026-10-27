# Interface-Display (arsip)

> **Repo ini diarsipkan dan bersifat _read-only_ sejak fase Tugas Akhir.** Antarmuka MoodIn kini dibangun dengan Flutter di [Interface-App](https://github.com/MoodInBME/Interface-App). Isi repo ini tidak dikembangkan lagi dan tidak mengikuti kontrak pesan versi TA.

Bagian dari proyek [MoodIn](https://github.com/MoodInBME/MoodIn-master). Isi repo ini sama dengan tag [`gemastik-xix-2026`](https://github.com/MoodInBME/Interface-Display/tree/gemastik-xix-2026), ditambah pembaruan README ini dan catatan arsip di `AGENTS.md`.

## Isi repo

| Bagian                  | Isi                                                                                                     | Catatan                                                      |
| ----------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| `src/moodin_interface/` | Aplikasi kiosk PySide6 + QML: layar idle, persetujuan, perekaman, hasil, tren, dan pengaturan           | Memakai kontrak pesan v1.1.0                                 |
| `web/`                  | Prototipe kiosk web (React + Vite) untuk layar _portrait_ 600×1024, termasuk layar Home Tamu dari Figma | Snapshot 8 Agustus 2026, belum diuji                         |
| `devkit/`               | Simulator MQTT untuk mengembangkan UI tanpa model (`tools/dev_simulator.py`)                            | —                                                            |
| `docs/`                 | Kontrak pesan v1.1.0 versi repo ini dan peta layar                                                      | Berbeda dari kontrak v1.0.0 di MoodIn-master                 |
| `tests/`                | Uji kontrak, basis data, dan _state machine_                                                            | —                                                            |
| `web/public/assets/`    | Aset SVG maskot dan ikon _mood_                                                                         | Boleh dipakai ulang di Interface-App dengan mencatat asalnya |

## Prinsip UI yang masih relevan untuk Interface-App

- Jangan menampilkan angka basi. Bila jalur fisiologis tidak tersedia, sembunyikan kartu tanda vital; jangan tampilkan nilai terakhir.
- Jangan menampilkan hasil dari jendela pengukuran yang belum penuh; tampilkan indikator kemajuan.
- Mode demo atau simulasi wajib diberi penanda yang selalu terlihat.
- Gunakan latar gelap dan kontras tinggi untuk tampilan di balik cermin dua arah, dan hindari elemen sentuh yang menuntut presisi.
- UI tidak menerima citra wajah; hanya nilai numerik.

## Lisensi

LGPL-3.0-or-later, mengikuti PySide6. Lihat [LICENSE](LICENSE). Dibuat oleh tim VisionaryX, Institut Teknologi Sepuluh Nopember, untuk GEMASTIK XIX 2026.
