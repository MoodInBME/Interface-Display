import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"
import "../theme"

Item {
    // Durasi minimal window akuisisi: >=30 detik (STC-rPPG).
    property int elapsed: 0
    readonly property int minWindow: 30

    ColumnLayout {
        anchors.centerIn: parent
        spacing: Theme.spacing
        width: parent.width * 0.8

        Text {
            text: "Menganalisis..."
            color: Theme.textPrimary
            font.pixelSize: Theme.fontTitle
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }
        Text {
            text: "Tetap diam menghadap cermin (" + elapsed + "/" + minWindow + " dtk)"
            color: Theme.textSecondary
            font.pixelSize: Theme.fontBody
            Layout.alignment: Qt.AlignHCenter
        }

        ProgressBar {
            from: 0; to: minWindow; value: elapsed
            Layout.fillWidth: true
        }

        SignalBadge { Layout.alignment: Qt.AlignHCenter }

        Text {
            visible: bridge.qualityMessage !== ""
            text: bridge.qualityMessage
            color: Theme.warning
            font.pixelSize: Theme.fontBody
            wrapMode: Text.WordWrap
            Layout.fillWidth: true
            horizontalAlignment: Text.AlignHCenter
        }

        PrimaryButton {
            text: "Batal"
            accent: Theme.danger
            Layout.alignment: Qt.AlignHCenter
            onClicked: bridge.cancelCapture()
        }
    }

    // Progress lokal; hasil final datang lewat bridge.resultChanged
    // yang otomatis pindah ke ResultScreen.
    Timer {
        interval: 1000
        running: true
        repeat: true
        onTriggered: if (elapsed < minWindow) elapsed += 1
    }
}
