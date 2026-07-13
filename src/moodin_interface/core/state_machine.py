"""State machine navigasi layar kiosk MoodIn."""
from __future__ import annotations

from enum import Enum


class Screen(str, Enum):
    SPLASH = "splash"
    IDLE_MIRROR = "idleMirror"
    ONBOARDING = "onboarding"
    MAIN_MENU = "mainMenu"
    CAPTURE = "capture"
    RESULT = "result"
    TRENDS = "trends"
    SETTINGS = "settings"


# Transisi legal: sumber -> himpunan tujuan yang diizinkan.
_TRANSITIONS: dict[Screen, set[Screen]] = {
    Screen.SPLASH: {Screen.IDLE_MIRROR, Screen.ONBOARDING},
    Screen.IDLE_MIRROR: {Screen.ONBOARDING, Screen.MAIN_MENU},
    Screen.ONBOARDING: {Screen.MAIN_MENU, Screen.IDLE_MIRROR},
    Screen.MAIN_MENU: {Screen.CAPTURE, Screen.TRENDS, Screen.SETTINGS, Screen.IDLE_MIRROR},
    Screen.CAPTURE: {Screen.RESULT, Screen.MAIN_MENU, Screen.IDLE_MIRROR},
    Screen.RESULT: {Screen.MAIN_MENU, Screen.TRENDS, Screen.CAPTURE, Screen.IDLE_MIRROR},
    Screen.TRENDS: {Screen.MAIN_MENU, Screen.IDLE_MIRROR},
    Screen.SETTINGS: {Screen.MAIN_MENU, Screen.IDLE_MIRROR},
}


class StateMachine:
    def __init__(self, initial: Screen = Screen.SPLASH) -> None:
        self._current = initial

    @property
    def current(self) -> Screen:
        return self._current

    def can_transition(self, target: Screen) -> bool:
        return target in _TRANSITIONS.get(self._current, set())

    def transition(self, target: Screen) -> bool:
        """Kembalikan True bila transisi berhasil, False bila ilegal."""
        if self.can_transition(target):
            self._current = target
            return True
        return False
