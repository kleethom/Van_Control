from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, "de_AT.UTF-8")

class ClockWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_time, 1)
        self.update_time(0)

    def update_time(self, dt):
        now = datetime.now()
        self.ids.time.text = now.strftime("%H:%M")
        self.ids.date.text = now.strftime("%A, %d.%m.%Y")