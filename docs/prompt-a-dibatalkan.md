# Prompt A - REVISI (ganti versi lama di PROMPTS.md)

## Kenapa Prompt A yang lama harus dibuang

Prompt A lama menyuruh model membangun `Theme.qml` dari `get_variable_defs`.
Asumsi itu salah. File desain MoodIn **tidak mendefinisikan satu pun Figma
Variable** - semua warna diketik langsung sebagai heksadesimal di level layer.
Jadi `{}` yang dikembalikan tool itu adalah **jawaban yang benar**, bukan
kegagalan koneksi, bukan salah seleksi, dan bukan soal Dev Mode.

Model Anda berperilaku persis seperti yang seharusnya: ia berhenti dan menolak
menebak warna. Instruksi berhentinya bekerja. Yang keliru adalah premis saya.

Bukti pendukung dari pemindaian ekspor SVG kemarin: 25 frame menghasilkan tepat
21 warna heksadesimal berbeda, tanpa satu pun referensi variable. Kalau desain
memakai variables, ekspor SVG akan menunjukkan pola berulang yang jauh lebih
sedikit.

## Penggantinya

`Theme.qml` sudah saya susun manual dari 21 warna itu, lengkap dengan jumlah
kemunculan tiap warna sebagai dasar penamaan semantik. **Prompt A tidak
dijalankan sama sekali.** Salin dua file berikut, lalu langsung ke Prompt B.

    src/moodin_interface/ui/Theme.qml
    src/moodin_interface/ui/qmldir

Daftarkan direktorinya di `app.py` sebelum memuat `Main.qml`:

    engine.addImportPath(os.path.join(os.path.dirname(__file__), "ui"))

lalu di setiap file QML yang butuh token:

    import MoodIn.Ui

## Tambahkan ini ke AGENTS.md bagian 5

> `Theme.qml` adalah sumber kebenaran palet, bukan Figma. File desain tidak
> memakai Figma Variables, sehingga `get_variable_defs` selalu mengembalikan
> `{}`. Jangan pernah memanggil tool itu lagi di proyek ini, dan jangan pernah
> menyimpulkan bahwa hasil kosongnya berarti ada yang rusak.

## Konsekuensi yang perlu Anda sadari

Tanpa variables, tidak ada jalur otomatis dari Figma ke kode. Kalau rekan
desainer mengubah satu warna di Figma, perubahan itu tidak akan sampai ke
aplikasi sampai ada yang mengetiknya ulang di `Theme.qml`. Untuk lomba dengan
tenggat dekat ini bukan masalah, dan membuat variables sekarang hanya menambah
pekerjaan. Cukup catat sebagai utang teknis.
