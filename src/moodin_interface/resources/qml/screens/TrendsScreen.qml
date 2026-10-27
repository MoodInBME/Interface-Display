import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"
import "../theme"

Item {
    property var moodData: []

    Component.onCompleted: moodData = bridge.loadTrends()

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: Theme.spacing
        spacing: Theme.spacing

        Text {
            text: "Tren Mood — 7 Hari Terakhir"
            color: Theme.textPrimary
            font.pixelSize: Theme.fontTitle
            font.bold: true
        }

        ListView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            model: moodData
            spacing: 8

            delegate: Rectangle {
                required property var modelData
                width: ListView.view.width
                height: 60
                radius: Theme.radius
                color: Theme.surface

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 12
                    spacing: 12

                    Rectangle {
                        width: 20; height: 20; radius: 10
                        color: Theme.moodColor(modelData.mood_id)
                        border.width: 2
                        border.color: Theme.moodDotBorder
                        antialiasing: true
                    }
                    Text {
                        text: modelData.mood_label
                        color: Theme.textPrimary
                        font.pixelSize: Theme.fontBody
                        Layout.preferredWidth: 120
                    }
                    Text {
                        text: modelData.created_at
                        color: Theme.textSecondary
                        font.pixelSize: Theme.fontBody
                        Layout.fillWidth: true
                    }
                    Text {
                        text: Math.round(modelData.confidence * 100) + "%"
                        color: Theme.textSecondary
                        font.pixelSize: Theme.fontBody
                    }
                }
            }
        }

        PrimaryButton {
            text: "Kembali"
            accent: Theme.warning
            textColor: Theme.warningDeep
            Layout.alignment: Qt.AlignHCenter
            onClicked: bridge.navigate("mainMenu")
        }
    }
}
