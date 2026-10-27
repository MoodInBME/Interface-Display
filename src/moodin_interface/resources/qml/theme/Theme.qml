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

    // ---------- Permukaan ----------
    // Palet mengikuti ekspor Figma bingkai 04-Home-Tamu: latar gradasi putih ke #DBF7FF,
    // dan teks warna gelap #3A3A3A.
    readonly property color backgroundGradientStart: "#FFFFFF"
    readonly property color backgroundGradientEnd:   "#DBF7FF"
    readonly property color background:    "#DBF7FF"
    readonly property color surface:       "#FFFFFF"
    readonly property color surfaceSunken: "#C9EEF7"

    // ---------- Teks ----------
    readonly property color textPrimary:   "#3A3A3A"
    readonly property color textSecondary: "#6B6B6B"
    readonly property color textOnAccent:  "#3A3A3A"

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
    readonly property color moodDotBorder: "#3A3A3A"
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
    readonly property int fontHuge:     56
    readonly property int fontTitle:    32
    readonly property int fontSubtitle: 26
    readonly property int fontBody:     20
    readonly property int fontCaption:  16

    // ---------- Jarak dan bentuk ----------
    readonly property int screenMargin: 56
    readonly property int spacing: 24
    readonly property int sp1: 4
    readonly property int sp2: 8
    readonly property int sp3: 16
    readonly property int sp4: 24
    readonly property int sp5: 32

    readonly property int radius:   18
    readonly property int radiusSm: 8
    readonly property int radiusLg: 28

    // Cermin disentuh sambil berdiri, sasarannya harus lebih besar.
    readonly property int touchTarget: 72
}
