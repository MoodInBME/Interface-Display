pragma Singleton
import QtQuick

// MoodIn - token desain tunggal.
// Lokasi: src/moodin_interface/resources/qml/theme/Theme.qml
// Diimpor dengan:  import "theme"      (module 'theme', lihat qmldir)
//
// ASAL NILAI WARNA
// Tidak diambil dari Figma Variables: file desain MoodIn tidak mendefinisikan
// satu pun variable, sehingga get_variable_defs selalu mengembalikan {}.
// Nilai di bawah adalah hasil pemindaian piksel atas 25 frame SVG hasil ekspor
// Figma. Angka pada komentar adalah jumlah kemunculan pada ekspor.
//
// KOMPATIBILITAS
// Semua nama properti versi lama dipertahankan (background, surface, primary,
// textPrimary, textSecondary, success, warning, danger, fontHuge, fontTitle,
// fontBody, radius, spacing, moodColor). Kedelapan layar memakainya.

QtObject {
    id: theme

    // displayMode adalah context property dari app.py: "kiosk" atau "windowed".
    readonly property bool isMirror: typeof displayMode !== "undefined"
                                     && displayMode === "kiosk"

    // ---------- Permukaan ----------
    // Palet cermin ditetapkan tim: #3A3A3A, BUKAN #0A0E12 versi lama.
    readonly property color background:    "#3A3A3A"  // 550x
    readonly property color surface:       "#505357"  // kartu di atas latar
    readonly property color surfaceSunken: "#1E1E1E"  // 6x

    // ---------- Teks ----------
    readonly property color textPrimary:   "#DBF7FF"  // 38x
    readonly property color textSecondary: "#A0A0A0"  // 82x
    readonly property color textOnAccent:  "#1E1E1E"

    // ---------- Aksen dan status ----------
    readonly property color primary:     "#48C2FF"  // 68x, biru interaktif
    readonly property color primaryDeep: "#2B7499"  // 2x, keadaan ditekan
    readonly property color success:     "#00AC46"  // 82x
    readonly property color successSoft: "#1EBC87"  // 2x
    readonly property color warning:     "#FFE46B"  // 42x
    readonly property color warningSoft: "#FFF1B1"  // 5x
    readonly property color warningDeep: "#6D5900"  // 28x, teks di atas kuning
    readonly property color danger:      "#FF9898"  // 97x
    readonly property color dangerSoft:  "#FFD8D8"  // 5x
    readonly property color dangerDeep:  "#7E2F2F"  // 10x, teks di atas merah
    readonly property color physio:      "#00F8C6"  // 6x, sinyal TTV
    readonly property color neutralChip: "#D9D9D9"  // 3x

    // ---------- Mood ----------
    // Indeks WAJIB sama dengan MOOD_CLASSES di labels.py:
    // 0 Ceria, 1 Cemas, 2 Tertekan, 3 Rileks, 4 Netral
    readonly property var moodColors: [
        "#FFE46B", "#FF9898", "#7E2F2F", "#48C2FF", "#A0A0A0"
    ]
    readonly property var moodLabels: [
        "Ceria", "Cemas", "Tertekan", "Rileks", "Netral"
    ]

    // moodId adalah INTEGER 0-4. Versi lama menerima string ("ceria") dan itu
    // melanggar kontrak IPC v1.1.0.
    function moodColor(moodId) {
        if (typeof moodId !== "number") {
            console.warn("Theme.moodColor: mood_id harus integer, diterima "
                         + typeof moodId + " = " + moodId)
            return textSecondary
        }
        return (moodId >= 0 && moodId < moodColors.length)
                ? moodColors[moodId] : textSecondary
    }

    function moodLabel(moodId) {
        return (typeof moodId === "number"
                && moodId >= 0 && moodId < moodLabels.length)
                ? moodLabels[moodId] : "Tidak diketahui"
    }

    // ---------- Tipografi ----------
    // Cermin dilihat dari ~55 cm, jendela dev dari ~30 cm.
    readonly property int fontHuge:     isMirror ? 56 : 34
    readonly property int fontTitle:    isMirror ? 32 : 24
    readonly property int fontSubtitle: isMirror ? 26 : 19
    readonly property int fontBody:     isMirror ? 20 : 15
    readonly property int fontCaption:  isMirror ? 16 : 12

    // ---------- Jarak dan bentuk ----------
    readonly property int spacing: 24
    readonly property int sp1: 4
    readonly property int sp2: 8
    readonly property int sp3: 16
    readonly property int sp4: 24
    readonly property int sp5: 32

    readonly property int radius:   18
    readonly property int radiusSm: 8
    readonly property int radiusLg: 24

    // Cermin disentuh sambil berdiri, sasarannya harus lebih besar.
    readonly property int touchTarget: isMirror ? 72 : 48
}
