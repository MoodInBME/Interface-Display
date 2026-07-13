import QtQuick
import QtQuick.Layouts
import "../components"
import "../theme"

Item {
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
                color: Theme.background
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
                accent: Theme.success
                onClicked: bridge.navigate("trends")
            }
            PrimaryButton {
                text: "Selesai"
                onClicked: bridge.navigate("mainMenu")
            }
        }
    }
}
