print(">>> gui/app.py GELADEN <<<")

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy_garden.graph import Graph, LinePlot

from gui.screens.main_screen import MainScreen
from gui.screens.history_screen import HistoryScreen

class VanKivyApp(App):
    def __init__(self, state, **kwargs):
        super().__init__(**kwargs)
        self.state = state
        print("GUI STATE-ID:", id(self.state))

    def build(self):
        #Builder.load_file("gui/van.kv")
        Builder.load_file("gui/kv/history_screen.kv")
        Builder.load_file("gui/kv/main_screen.kv")

        sm = ScreenManager()

        sm.add_widget(MainScreen(name="main", state=self.state))
        sm.add_widget(HistoryScreen(name="history", state=self.state))

        return sm