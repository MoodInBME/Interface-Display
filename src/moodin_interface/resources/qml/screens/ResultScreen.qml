import QtQuick
import QtQuick.Layouts
import "../components"
import "../theme"

Item {
    Rectangle {
        visible: bridge.simulated
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        height: bannerText.implicitHeight + (Theme.sp2 * 2)
        color: Theme.warning
        // Aturan: tambahkan radiusSm sesuai permintaan
        radius: Theme.radiusSm

        Text {
            id: bannerText
            anchors.centerIn: parent
            text: "DATA SIMULASI - BUKAN HASIL PENGUKURAN"
            color: Theme.warningDeep
            font.pixelSize: Theme.fontCaption
        }
    }

    ColumnLayout {
        anchors.centerIn: parent
        spacing: Theme.spacing
        width: parent.width * 0.8

        Rectangle {
            width: 160; height: 160; radius: 80
            color: Theme.moodColor(bridge.moodId)
            Layout.alignment: Qt.AlignHCenter
            Text {
                anchors.centerIn: parent
                text: bridge.moodLabel
                color: Theme.textPrimary
                font.pixelSize: Theme.fontTitle
                font.bold: true
            }
        }

        Text {
            text: "Keyakinan: " + Math.round(bridge.confidence * 100) + "%"
            color: Theme.textSecondary
            font.pixelSize: Theme.fontBody
            Layout.alignment: Qt.AlignHCenter
        }
        Text {
            visible: bridge.heartRate > 0
            text: "Denyut: " + Math.round(bridge.heartRate) + " bpm"
            color: Theme.textSecondary
            font.pixelSize: Theme.fontBody
            Layout.alignment: Qt.AlignHCenter
        }

        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            spacing: Theme.spacing
            PrimaryButton {
                text: "Lihat Tren"
                accent: Theme.primary
                textColor: Theme.textOnAccent
                onClicked: bridge.navigate("trends")
            }
            PrimaryButton {
                text: "Selesai"
                accent: Theme.warning
                textColor: Theme.warningDeep
                onClicked: bridge.navigate("mainMenu")
            }
        }
    }
}
