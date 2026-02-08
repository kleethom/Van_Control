from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from datetime import datetime
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
import locale

locale.setlocale(locale.LC_TIME, "de_AT.UTF-8")

class MainScreen(Screen):
    state = ObjectProperty()

    def on_kv_post(self, base_widget):
        Clock.schedule_interval(self.update_time, 1)
        self.update_time(0)

    def update_time(self, dt):
        now = datetime.now()
        self.ids.time.text = now.strftime("%H:%M:%S")
        self.ids.date.text = now.strftime("%A, %d.%m.%Y")

class ClickableBox(ButtonBehavior, BoxLayout):
    pass