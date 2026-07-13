import QtQuick
import QtQuick.Layouts
import "../components"
import "../theme"

Item {
    ColumnLayout {
        anchors.centerIn: parent
        spacing: Theme.spacing
        width: parent.width * 0.7

        Text {
            text: "Pengaturan"
            color: Theme.textPrimary
            font.pixelSize: Theme.fontTitle
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }

        RowLayout {
            Layout.fillWidth: true
            Text {
                text: "Status koneksi sistem"
                color: Theme.textSecondary
                font.pixelSize: Theme.fontBody
                Layout.fillWidth: true
            }
            Text {
                text: bridge.brokerConnected ? "Terhubung" : "Terputus"
                color: bridge.brokerConnected ? Theme.success : Theme.danger
                font.pixelSize: Theme.fontBody
            }
        }

        SignalBadge { Layout.alignment: Qt.AlignLeft }

        PrimaryButton {
            text: "Kembali"
            accent: Theme.textSecondary
            Layout.alignment: Qt.AlignHCenter
            onClicked: bridge.navigate("mainMenu")
        }
    }
}
