import QtQuick
import QtQuick.Layouts
import "../components"
import "../theme"

Item {
    id: root

    // Avatar dan "Sign Up" (Tamu placeholder)
    ColumnLayout {
        id: avatarCol
        anchors.top: parent.top
        anchors.topMargin: Theme.spacing
        anchors.right: parent.right
        anchors.rightMargin: Theme.spacing * 2
        spacing: Theme.sp1

        Rectangle {
            Layout.preferredWidth: Theme.touchTarget
            Layout.preferredHeight: Theme.touchTarget
            radius: width / 2
            color: Theme.success
            Layout.alignment: Qt.AlignHCenter

            Text {
                anchors.centerIn: parent
                text: "?"
                color: Theme.textOnAccent
                font.pixelSize: Theme.fontTitle
                font.bold: true
            }
        }

        Text {
            text: "Daftar lewat aplikasi MoodIn"
            color: Theme.textSecondary
            font.pixelSize: Theme.fontCaption
            Layout.alignment: Qt.AlignHCenter
            Layout.maximumWidth: Theme.touchTarget * 3
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignHCenter
        }
    }

    ColumnLayout {
        anchors.top: avatarCol.bottom
        anchors.topMargin: Theme.spacing
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.leftMargin: Theme.screenMargin
        anchors.rightMargin: Theme.screenMargin
        anchors.bottomMargin: Theme.screenMargin
        spacing: Theme.spacing

        // Header
        ColumnLayout {
            spacing: Theme.sp2
            Layout.fillWidth: true

            Text {
                text: "Halo, User!"
                color: Theme.textPrimary
                font.pixelSize: Theme.fontHuge
                font.bold: true
                Layout.fillWidth: true
                wrapMode: Text.WordWrap
            }

            Text {
                text: "Apa yang ingin kamu lakukan hari ini?"
                color: Theme.textSecondary
                font.pixelSize: Theme.fontSubtitle
                Layout.fillWidth: true
                wrapMode: Text.WordWrap
            }
        }

        Item { Layout.preferredHeight: Theme.sp2 }

        PrimaryButton {
            id: btnCapture
            font.pixelSize: Theme.fontTitle
            Layout.fillWidth: true
            Layout.preferredHeight: Theme.touchTarget * 2.5
            accent: Theme.danger
            textColor: Theme.textPrimary
            text: "Deteksi Mood"
            subtitle: "Deteksi moodmu sekarang!"
            iconOnLeft: false
            enabled: bridge.brokerConnected
            onClicked: bridge.startCapture()

            iconSlot: Component {
                Item {
                    readonly property real assetRatio: 255 / 247 // rasio asli ~1.03:1
                    readonly property real maxHeight: (Theme.touchTarget * 2.5) - (2 * Theme.sp2)
                    implicitHeight: Math.min(247, maxHeight > 0 ? maxHeight : 247)
                    implicitWidth: implicitHeight * assetRatio
                    // TODO ikon: Group 49
                }
            }
        }

        PrimaryButton {
            id: btnTrends
            font.pixelSize: Theme.fontTitle
            Layout.fillWidth: true
            Layout.preferredHeight: Theme.touchTarget * 2.5
            Layout.topMargin: Theme.sp2
            accent: Theme.primary
            textColor: Theme.textOnAccent
            text: "Tren 7 Hari"
            subtitle: "Lihat tren mingguanmu!"
            iconOnLeft: true
            onClicked: bridge.navigate("trends")

            iconSlot: Component {
                Item {
                    readonly property real assetRatio: 1.0 // rasio asli 283/283
                    readonly property real maxHeight: (Theme.touchTarget * 2.5) - (2 * Theme.sp2)
                    implicitHeight: Math.min(283, maxHeight > 0 ? maxHeight : 283)
                    implicitWidth: implicitHeight * assetRatio
                    // TODO ikon: Group 52
                }
            }
        }

        // Area Bawah (Pengaturan, Kembali, Maskot)
        RowLayout {
            Layout.topMargin: Theme.sp5
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.minimumHeight: (Theme.touchTarget * 2) + Theme.spacing
            spacing: 0

            ColumnLayout {
                Layout.preferredWidth: Theme.touchTarget * 3
                Layout.maximumWidth: Theme.touchTarget * 3
                Layout.fillHeight: true
                spacing: Theme.sp3

                PrimaryButton {
                    id: btnSettings
                    Layout.fillWidth: true
                    Layout.preferredHeight: Theme.touchTarget + Theme.spacing
                    accent: Theme.warning
                    textColor: Theme.warningDeep
                    text: "Pengaturan"
                    iconOnLeft: false
                    onClicked: bridge.navigate("settings")

                    // TODO Group 58 adalah overlay latar tombol penuh 215x94, tangani lewat properti background bukan iconSlot
                }

                PrimaryButton {
                    id: btnBack
                    Layout.fillWidth: true
                    Layout.preferredHeight: Theme.touchTarget + Theme.spacing
                    accent: Theme.warning
                    textColor: Theme.warningDeep
                    text: "Kembali"
                    iconOnLeft: false
                    onClicked: bridge.navigate("idleMirror")
                    // TODO gradasi menunggu token Theme

                    // TODO Group 59 adalah overlay latar tombol penuh 215x94, tangani lewat properti background bukan iconSlot
                }
            }

            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.rightMargin: -Theme.screenMargin
                
                Item {
                    anchors.right: parent.right
                    anchors.bottom: parent.bottom
                    readonly property real assetRatio: 331 / 283
                    
                    // Batasi tinggi berdasarkan lebar agar tidak meluber
                    readonly property real hBoundByWidth: parent.width / assetRatio
                    readonly property real hBoundByHeight: parent.height
                    
                    height: Math.min(283, Math.min(hBoundByHeight, hBoundByWidth))
                    width: height * assetRatio
                    // TODO maskot: Group 56
                }
            }
        }

        Rectangle {
            visible: !bridge.brokerConnected
            Layout.fillWidth: true
            Layout.preferredHeight: warningText.implicitHeight + (Theme.sp2 * 2)
            color: Theme.danger
            radius: Theme.radiusSm

            Text {
                id: warningText
                anchors.centerIn: parent
                width: parent.width - (Theme.sp2 * 2)
                text: "⚠ Tidak terhubung ke sistem — deteksi nonaktif"
                color: Theme.textPrimary
                font.pixelSize: Theme.fontBody
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
            }
        }
    }
}
