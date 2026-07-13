import QtQuick
import "../theme"

Item {
    // Mode cermin: latar gelap dominan agar reflektif; UI minimal.
    Column {
        anchors.centerIn: parent
        spacing: Theme.spacing
        opacity: bridge.userPresent ? 1.0 : 0.35
        Behavior on opacity { NumberAnimation { duration: 400 } }

        Text {
            id: clockLabel
            text: Qt.formatDateTime(new Date(), "HH:mm")
            color: Theme.textPrimary
            font.pixelSize: Theme.fontHuge
            anchors.horizontalCenter: parent.horizontalCenter
        }
        Text {
            text: bridge.userPresent ? "Sentuh untuk memulai" : "Mendekatlah ke cermin"
            color: Theme.textSecondary
            font.pixelSize: Theme.fontBody
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }

    // Perbarui jam tiap detik.
    Timer {
        interval: 1000
        running: true
        repeat: true
        onTriggered: clockLabel.text = Qt.formatDateTime(new Date(), "HH:mm")
    }

    MouseArea {
        anchors.fill: parent
        enabled: bridge.userPresent
        onClicked: bridge.navigate("mainMenu")
    }
}
