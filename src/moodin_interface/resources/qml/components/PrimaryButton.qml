import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../theme"

Button {
    id: control
    property color accent: Theme.primary
    property color textColor: Theme.background
    property string subtitle: ""
    property Component iconSlot: null
    property bool iconOnLeft: false

    implicitHeight: 64
    implicitWidth: 220
    font.pixelSize: Theme.fontBody

    contentItem: Item {
        implicitWidth: layout.implicitWidth
        implicitHeight: layout.implicitHeight

        RowLayout {
            id: layout
            anchors.fill: parent
            spacing: Theme.spacing

            Loader {
                active: control.iconSlot !== null && control.iconOnLeft
                visible: active
                sourceComponent: control.iconSlot
                Layout.alignment: Qt.AlignVCenter
                Layout.preferredWidth: item ? item.implicitWidth : 0
                Layout.preferredHeight: item ? item.implicitHeight : 0
            }

            ColumnLayout {
                spacing: Theme.sp1
                Layout.fillWidth: true

                Text {
                    text: control.text
                    color: control.textColor
                    font: control.font
                    horizontalAlignment: control.iconSlot !== null ? (control.iconOnLeft ? Text.AlignRight : Text.AlignLeft) : Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    Layout.fillWidth: true
                    wrapMode: Text.WordWrap
                }

                Text {
                    visible: control.subtitle !== ""
                    text: control.subtitle
                    color: control.textColor
                    font.pixelSize: Theme.fontBody
                    horizontalAlignment: control.iconSlot !== null ? (control.iconOnLeft ? Text.AlignRight : Text.AlignLeft) : Text.AlignHCenter
                    Layout.fillWidth: true
                    wrapMode: Text.WordWrap
                }
            }

            Loader {
                active: control.iconSlot !== null && !control.iconOnLeft
                visible: active
                sourceComponent: control.iconSlot
                Layout.alignment: Qt.AlignVCenter
                Layout.preferredWidth: item ? item.implicitWidth : 0
                Layout.preferredHeight: item ? item.implicitHeight : 0
            }
        }
    }

    background: Rectangle {
        radius: Theme.radius
        color: control.down ? Qt.darker(control.accent, 1.2) : control.accent
        opacity: control.enabled ? 1.0 : 0.4
    }
}
