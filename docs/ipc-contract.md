# Kontrak IPC MoodIn (v1.1.0)

Semua komunikasi antar-repo lewat MQTT broker (TLS, port 8883 di produksi;
`localhost:1883` tanpa TLS untuk pengembangan lokal).

Sumber kebenaran skema: `src/moodin_interface/ipc/contracts.py` di repo ini,
DAN `communication/topics.py` + `communication/contracts.py` di repo
`Software-Architecture`. Keduanya harus dijaga tetap sama.

## Riwayat versi

| Versi | Perubahan |
|-------|-----------|
| 1.0.0 | Rilis awal. `mood_id` bertipe string. |
| 1.1.0 | `mood_id` menjadi **integer 0..4**. Tambah `physio_used` dan `simulated`. |

## Topik

| Topik | Arah | Publisher | Subscriber | QoS | Retain |
|-------|------|-----------|------------|-----|--------|
| `moodin/inference/result` | hasil mood | Software-Architecture | Interface-Display | 1 | tidak |
| `moodin/signal/quality`   | mutu sinyal rPPG | Hardware/Software | Interface-Display | 0 | tidak |
| `moodin/presence`         | kehadiran user | Hardware-Connections | Interface-Display | 1 | ya |
| `moodin/ui/command`       | perintah UI | Interface-Display | Hardware/Software | 1 | tidak |

## Skema payload (JSON)

### moodin/inference/result

    {
      "mood_id": 3,
      "mood_label": "Rileks",
      "confidence": 0.87,
      "valence": 0.6,
      "arousal": -0.3,
      "heart_rate_bpm": 72.5,
      "hrv_ms": 45.2,
      "physio_used": true,
      "simulated": false,
      "session_id": "abc123",
      "version": "1.1.0"
    }

**`mood_id` adalah INTEGER, bukan string.** Pemetaannya ditentukan oleh
`MOOD_CLASSES` di `Software-Architecture/models/st_gcn_graph_tran/labels.py`,
karena repo itulah yang menerbitkan pesan:

| `mood_id` | label |
|-----------|-------|
| 0 | Ceria |
| 1 | Cemas |
| 2 | Tertekan |
| 3 | Rileks |
| 4 | Netral |

String seperti `"rileks"` **tidak valid** di v1.1.0. Fungsi `_mood_id()` di
`contracts.py` masih menerjemahkannya sebagai jaring pengaman sementara, tetapi
mencatat peringatan; jangan menjadikannya jalur normal.

`physio_used: false` berarti nilai TTV tidak dapat dipercaya dan kartu TTV harus
disembunyikan, bukan menampilkan angka lama.

`simulated: true` berarti keluaran berasal dari DEMO_MODE di `inference.py` dan
bukan hasil pengukuran wajah. UI wajib menampilkan pita peringatan permanen.

### moodin/signal/quality

    { "quality": 0.72, "face_detected": true, "illumination_ok": true, "message": "" }

### moodin/presence

    { "present": true, "distance_cm": 35.0 }

### moodin/ui/command

    { "command": "start_capture", "ts": "2026-07-13T07:14:00Z" }

`command` salah satu dari: `start_capture`, `cancel_capture`.

## Aturan degradasi UI

| Kondisi | Perilaku wajib |
|---------|----------------|
| `simulated == true` | pita peringatan permanen |
| `physio_used == false` | sembunyikan kartu TTV |
| `face_detected == false` lebih dari 3 detik | kembali ke `idleMirror` |
| `quality < 1.0` | cincin progres pengisian buffer |
| presence `offline` | banner terputus, tombol deteksi dinonaktifkan |
| `confidence < 0.5` | tanda ketidakpastian di samping label mood |

## Versi dan kompatibilitas

Perubahan skema harus menaikkan versi dokumen ini dan disepakati oleh ketiga
repo lain sebelum di-deploy.
