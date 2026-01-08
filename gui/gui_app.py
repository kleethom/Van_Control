print(">>> gui/app.py GELADEN <<<")

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from gui.main_screen import MainScreen

class VanKivyApp(App):
    def __init__(self, state, **kwargs):
        super().__init__(**kwargs)
        self.state = state
        print("GUI STATE-ID:", id(self.state))

    def build(self):
        Builder.load_file("gui/van.kv")

        sm = ScreenManager()

        main_screen = MainScreen(name="main", state=self.state)

        sm.add_widget(main_screen)
        return sm