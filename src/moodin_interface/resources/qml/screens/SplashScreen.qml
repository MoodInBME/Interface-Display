import QtQuick
import "../theme"

Item {
    Column {
        anchors.centerIn: parent
        spacing: Theme.spacing

        Text {
            text: "MoodIn"
            color: Theme.primary
            font.pixelSize: Theme.fontHuge
            font.bold: true
            anchors.horizontalCenter: parent.horizontalCenter
        }
        Text {
            text: "Personal Wellness Coach"
            color: Theme.textSecondary
            font.pixelSize: Theme.fontBody
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }

    // Auto-lanjut ke IdleMirror setelah boot.
    Timer {
        interval: 2500
        running: true
        repeat: false
        onTriggered: bridge.navigate("idleMirror")
    }
}
