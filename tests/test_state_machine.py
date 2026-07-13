from moodin_interface.core.state_machine import Screen, StateMachine


def test_initial_state_is_splash():
    sm = StateMachine()
    assert sm.current is Screen.SPLASH


def test_legal_transition_succeeds():
    sm = StateMachine(Screen.MAIN_MENU)
    assert sm.transition(Screen.CAPTURE) is True
    assert sm.current is Screen.CAPTURE


def test_illegal_transition_is_rejected():
    sm = StateMachine(Screen.SPLASH)
    assert sm.transition(Screen.CAPTURE) is False
    assert sm.current is Screen.SPLASH


def test_capture_to_result_flow():
    sm = StateMachine(Screen.CAPTURE)
    assert sm.transition(Screen.RESULT) is True
    assert sm.transition(Screen.TRENDS) is True
