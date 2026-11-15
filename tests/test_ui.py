from pathlib import Path
from streamlit.testing.v1 import AppTest

def button(app,label):
    return next(b for b in app.button if b.label == label)

def test_confirmation_cancel_restart_switch():
    app = AppTest.from_file(Path(__file__).resolve().parents[1] / 'app.py').run()
    assert not app.exception
    app.chat_input[0].set_value('enter 3142 on drawer').run()
    assert not app.session_state['game'].drawer_open
    button(app,'Cancel action').click().run()
    assert not app.session_state['game'].drawer_open
    app.chat_input[0].set_value('enter 3142 on drawer').run()
    button(app,'Confirm action').click().run()
    assert app.session_state['game'].drawer_open
    button(app,'Restart game').click().run()
    assert not app.session_state['game'].drawer_open
    app.selectbox[0].select('Version 1 — Baseline').run()
    assert app.chat_input[0].disabled
    assert not app.exception

def test_full_ui_walkthrough():
    app = AppTest.from_file(Path(__file__).resolve().parents[1] / 'app.py').run()
    for command in ['examine bookshelf','enter 3142 on drawer','take key','use key on desk',
                    'answer time','take note','examine painting','enter 5826 on door']:
        app.chat_input[0].set_value(command).run()
        button(app,'Confirm action').click().run()
    assert app.session_state['game'].escaped and app.chat_input[0].disabled
    assert not app.exception
