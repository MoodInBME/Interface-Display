# PROMPTS.md - urutan prompt untuk Antigravity CLI

Jalankan dari dalam workspace `Interface-Display`, dengan Figma Desktop terbuka
dan file MoodIn aktif (server MCP lokal di `http://127.0.0.1:3845/mcp` hanya
bekerja terhadap seleksi di aplikasi desktop).

Urutannya penting. Prompt B tidak akan menghasilkan apa pun yang berguna sebelum
Prompt A selesai, karena `Theme` belum ada.

---

## Prompt A - bangun Theme.qml dari Figma variables

Jalankan sekali saja. Pilih satu frame apa pun di Figma lebih dulu.

    Baca AGENTS.md di repo ini lebih dulu, khususnya bagian 3, 5, dan 8.

    Tugas: buat src/moodin_interface/ui/Theme.qml sebagai singleton QML.

    Langkah:
    1. Panggil get_variable_defs pada seleksi Figma saat ini untuk mengambil
       seluruh variabel warna dan tipografi yang terdefinisi.
    2. Kalau get_variable_defs mengembalikan kosong atau sangat sedikit,
       BERHENTI dan laporkan apa yang kamu dapat. Jangan menebak warna.
    3. Petakan setiap variabel ke satu readonly property di Theme.qml.
       Pertahankan nama semantik dari Figma, bukan nama warna literal.
       Contoh: "surface/base" menjadi surfaceBase, bukan abuGelap.
    4. Tambahkan properti isMirror dan skala tipografi bercabang seperti pada
       AGENTS.md bagian 5.
    5. Daftarkan singleton-nya lewat qmldir di direktori yang sama.

    Keluaran: Theme.qml, qmldir, dan satu tabel ringkas yang memetakan nama
    variabel Figma ke nama properti QML. Jangan sentuh file lain.

---

## Prompt B - satu layar per kali

Ulangi untuk tiap frame. Ganti dua nilai di baris pertama. Pilih frame yang
bersangkutan di Figma sebelum menjalankan.

    Frame Figma: 04-Home-Tamu
    File target: src/moodin_interface/ui/screens/HomeTamu.qml

    Baca AGENTS.md lebih dulu. Bagian 3 adalah larangan keras, patuhi semuanya.

    Langkah:
    1. Panggil get_screenshot pada seleksi saat ini supaya kamu melihat tata
       letak yang dituju.
    2. Panggil get_metadata untuk memperoleh hierarki node, nama layer, dan
       kotak batas. Pakai ini untuk menyimpulkan struktur, bukan untuk menyalin
       koordinat.
    3. JANGAN panggil get_design_context. Tool itu mengembalikan React dan akan
       menyesatkanmu.
    4. Tulis file QML-nya. Root harus Item dengan anchors.fill: parent.
       Semua tata letak lewat ColumnLayout / RowLayout / anchors.
       Semua warna lewat Theme. Semua ukuran font lewat Theme.
    5. Setiap teks yang berasal dari data runtime harus terikat ke properti
       bridge, bukan string tetap. Kalau properti bridge yang dibutuhkan belum
       ada, deklarasikan property alias di bagian atas file dan CATAT di
       ringkasan akhir; jangan diam-diam menambah slot di bridge.py.
    6. Elemen yang jelas akan berulang di layar lain, pindahkan ke
       ui/components/ sebagai komponen tersendiri.

    Setelah menulis, verifikasi sendiri terhadap AGENTS.md bagian 8 dan laporkan
    poin mana yang belum terpenuhi. Jangan mengklaim selesai kalau ada yang
    gagal.

---

## Prompt C - sambungkan ke bridge dan aturan degradasi

Jalankan setelah 4-5 layar pertama jadi, jangan menunggu 25 layar selesai.

    Baca AGENTS.md bagian 6 dan docs/ipc-contract.md.

    Ada dua sumber kontrak IPC yang saling bertentangan di organisasi ini.
    Yang BENAR adalah mood_id bertipe integer 0-4, sesuai labels.py di repo
    Software-Architecture. Kalau docs/ipc-contract.md di repo ini masih menulis
    mood_id sebagai string, perbaiki dokumennya, bukan kodenya.

    Tugas:
    1. Perluas core/bridge.py agar mengekspos properti Qt untuk setiap field
       payload di AGENTS.md bagian 6, termasuk field baru simulated.
    2. Implementasikan keenam aturan degradasi di AGENTS.md bagian 6 sebagai
       state yang dapat dibaca QML, bukan sebagai logika if di dalam QML.
    3. Tambahkan pita peringatan simulated di Main.qml dengan teks
       MODE DEMO - NILAI DISIMULASIKAN
    4. Perbarui ipc/contracts.py agar cocok, dan naikkan CONTRACT_VERSION
       menjadi 1.1.0

    Setelah itu jalankan devkit/tools/dev_simulator.py dan tunjukkan bahwa
    keenam aturan degradasi benar-benar memicu perubahan tampilan.

---

## Prompt D - pemeriksaan mandiri sebelum commit

    Baca AGENTS.md bagian 3 dan 8.

    Periksa seluruh file di src/moodin_interface/ui/ dan laporkan sebagai tabel:
    nama file, jumlah literal warna heksadesimal, jumlah properti x atau y yang
    dipakai untuk tata letak, jumlah ukuran font berupa angka mentah, dan
    apakah root-nya Item.

    Jangan perbaiki apa pun dulu. Tampilkan tabelnya saja, lalu tunggu
    persetujuan saya sebelum mengubah file.

    Terakhir, jalankan aplikasi dua kali, sekali dengan appWidth 600 appHeight
    1024 dan sekali dengan 400x900, lalu laporkan warning QML apa pun yang
    muncul di konsol.

---

## Catatan penggunaan Figma MCP

get_design_context adalah jebakan di proyek ini. Tool itu dirancang untuk
menghasilkan React plus Tailwind. Model akan tergoda memakainya karena itulah
tool paling kaya informasi. Larangan di AGENTS.md bagian 3 nomor 1 ada khusus
untuk mencegahnya, dan Prompt B mengulanginya secara eksplisit karena satu
larangan saja sering tidak cukup.

Kombinasi yang benar untuk QML adalah get_screenshot sebagai acuan visual,
ditambah get_metadata untuk hierarki dan nama layer. Dari keduanya, struktur
ColumnLayout yang wajar bisa disimpulkan tanpa menyalin koordinat.

Seleksi di Figma Desktop menentukan lingkup semua tool ini. Kalau tidak ada yang
terpilih, lingkupnya menjadi seluruh halaman dan keluarannya akan terpotong.
Pilih tepat satu frame sebelum menjalankan Prompt B.

## Urutan pengerjaan yang disarankan

Jangan mulai dari frame nomor 01. Mulailah dari layar yang paling banyak
melahirkan komponen bersama, supaya sisanya menjadi murah:

1. 04-Home-Tamu, melahirkan kartu, tombol utama, header
2. 07-Deteksi-Hasil-01, melahirkan kartu mood, kartu TTV, indikator keyakinan
3. 03-Scan-Idle, melahirkan cincin progres dan status kamera
4. 08-Tren-7Hari, melahirkan grafik, satu-satunya komponen yang benar-benar sulit
5. 17-Pengaturan, melahirkan baris daftar dan sakelar

Setelah kelimanya jadi, dua puluh layar sisanya sebagian besar hanya menyusun
ulang komponen yang sudah ada.
