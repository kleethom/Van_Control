from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from gui.main_screen import MainScreen

class VanKivyApp(App):
    def __init__(self, state, **kwargs):
        super().__init__(**kwargs)
        self.state = state

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        return sm