import QtQuick
import QtQuick.Window
import QtQuick.Controls
import "screens" as Screens
import "theme"

Window {
    id: root
    visible: true
    width: appWidth
    height: appHeight
    color: Theme.background
    title: "MoodIn"

    // Kiosk fullscreen; windowed untuk dev.
    visibility: displayMode === "kiosk" ? Window.FullScreen : Window.Windowed

    // Peta screen -> komponen.
    function screenSource(name) {
        switch (name) {
            case "splash":      return splash;
            case "idleMirror":  return idleMirror;
            case "onboarding":  return onboarding;
            case "mainMenu":    return mainMenu;
            case "capture":     return capture;
            case "result":      return result;
            case "trends":      return trends;
            case "settings":    return settings;
            default:            return splash;
        }
    }

    StackView {
        id: stack
        anchors.fill: parent
        initialItem: splash
    }

    // Reaksi terhadap perubahan layar dari bridge (state machine Python).
    Connections {
        target: bridge
        function onScreenChanged() {
            stack.replace(root.screenSource(bridge.currentScreen));
        }
    }

    // Timer idle: kembali ke IdleMirror setelah tidak ada interaksi.
    Timer {
        id: idleTimer
        interval: 45000
        running: bridge.currentScreen !== "idleMirror"
                 && bridge.currentScreen !== "splash"
        repeat: false
        onTriggered: bridge.navigate("idleMirror")
    }

    MouseArea {
        anchors.fill: parent
        propagateComposedEvents: true
        onPressed: function(mouse) { idleTimer.restart(); mouse.accepted = false; }
    }

    // Definisi komponen layar (lazy).
    Component { id: splash;      Screens.SplashScreen {} }
    Component { id: idleMirror;  Screens.IdleMirror {} }
    Component { id: onboarding;  Screens.OnboardingConsent {} }
    Component { id: mainMenu;    Screens.MainMenu {} }
    Component { id: capture;     Screens.CaptureScreen {} }
    Component { id: result;      Screens.ResultScreen {} }
    Component { id: trends;      Screens.TrendsScreen {} }
    Component { id: settings;    Screens.SettingsScreen {} }
}
