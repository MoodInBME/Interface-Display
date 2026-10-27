import QtQuick
import "../theme"

Row {
    spacing: 8
    property real quality: bridge.signalQuality

    Rectangle {
        width: 14; height: 14; radius: 7
        anchors.verticalCenter: parent.verticalCenter
        color: quality >= 0.6 ? Theme.success
             : quality >= 0.3 ? Theme.warning
             : Theme.danger
    }
    Text {
        text: "Sinyal: " + Math.round(quality * 100) + "%"
        color: Theme.textPrimary
        font.pixelSize: Theme.fontBody
    }
}
