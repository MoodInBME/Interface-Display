import QtQuick
import QtQuick.Layouts
import "../components"
import "../theme"

Item {
    ColumnLayout {
        anchors.centerIn: parent
        spacing: Theme.spacing

        Text {
            text: "Menu Utama"
            color: Theme.textPrimary
            font.pixelSize: Theme.fontTitle
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }

        GridLayout {
            columns: 2
            rowSpacing: Theme.spacing
            columnSpacing: Theme.spacing
            Layout.alignment: Qt.AlignHCenter

            PrimaryButton {
                text: "Deteksi Mood"
                enabled: bridge.brokerConnected
                onClicked: bridge.startCapture()
            }
            PrimaryButton {
                text: "Tren 7 Hari"
                accent: Theme.success
                onClicked: bridge.navigate("trends")
            }
            PrimaryButton {
                text: "Pengaturan"
                accent: Theme.textSecondary
                onClicked: bridge.navigate("settings")
            }
            PrimaryButton {
                text: "Kembali"
                accent: Theme.textSecondary
                onClicked: bridge.navigate("idleMirror")
            }
        }

        Text {
            visible: !bridge.brokerConnected
            text: "⚠ Tidak terhubung ke sistem — deteksi nonaktif"
            color: Theme.danger
            font.pixelSize: Theme.fontBody
            Layout.alignment: Qt.AlignHCenter
        }
    }
}
