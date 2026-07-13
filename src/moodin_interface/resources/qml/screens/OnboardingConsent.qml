import QtQuick
import QtQuick.Layouts
import "../components"
import "../theme"

Item {
    ColumnLayout {
        anchors.centerIn: parent
        width: parent.width * 0.8
        spacing: Theme.spacing

        Text {
            text: "Persetujuan Data Biometrik"
            color: Theme.textPrimary
            font.pixelSize: Theme.fontTitle
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }
        Text {
            // Pemenuhan UU PDP No.27/2022 - consent eksplisit.
            text: "MoodIn memproses sinyal wajah dan denyut (rPPG) secara lokal " +
                  "di perangkat untuk mengklasifikasikan mood Anda. Data tidak " +
                  "dikirim ke server eksternal. Anda dapat menghapus riwayat kapan saja."
            color: Theme.textSecondary
            font.pixelSize: Theme.fontBody
            wrapMode: Text.WordWrap
            Layout.fillWidth: true
            horizontalAlignment: Text.AlignHCenter
        }
        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            spacing: Theme.spacing
            PrimaryButton {
                text: "Setuju & Lanjut"
                onClicked: bridge.navigate("mainMenu")
            }
            PrimaryButton {
                text: "Batal"
                accent: Theme.textSecondary
                onClicked: bridge.navigate("idleMirror")
            }
        }
    }
}
