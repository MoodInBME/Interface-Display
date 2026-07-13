pragma Singleton
import QtQuick

QtObject {
    // Palet gelap untuk two-way mirror (teks terang di latar gelap
    // memaksimalkan kontras di balik cermin).
    readonly property color background: "#0A0E12"
    readonly property color surface:    "#141A21"
    readonly property color primary:    "#4FD1C5"
    readonly property color textPrimary:   "#F5F7FA"
    readonly property color textSecondary: "#9AA6B2"
    readonly property color danger:  "#F87171"
    readonly property color warning: "#FBBF24"
    readonly property color success: "#34D399"

    // Warna per kuadran mood (valence-arousal).
    function moodColor(moodId) {
        switch (moodId) {
            case "ceria":    return "#FBBF24";
            case "cemas":    return "#F87171";
            case "tertekan": return "#818CF8";
            case "rileks":   return "#34D399";
            default:         return "#9AA6B2"; // netral
        }
    }

    readonly property int fontHuge:  56
    readonly property int fontTitle: 32
    readonly property int fontBody:  20
    readonly property int radius:    18
    readonly property int spacing:   24
}
