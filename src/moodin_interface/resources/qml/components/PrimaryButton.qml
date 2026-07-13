import QtQuick
import QtQuick.Controls
import "../theme"

Button {
    id: control
    property color accent: Theme.primary
    implicitHeight: 64
    implicitWidth: 220
    font.pixelSize: Theme.fontBody

    contentItem: Text {
        text: control.text
        color: Theme.background
        font: control.font
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }

    background: Rectangle {
        radius: Theme.radius
        color: control.down ? Qt.darker(control.accent, 1.2) : control.accent
        opacity: control.enabled ? 1.0 : 0.4
    }
}
