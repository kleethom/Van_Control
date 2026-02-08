from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy_garden.graph import LinePlot
from gui.data.history_provider import HistoryProvider
import time
from datetime import datetime, timedelta, timezone
from kivy.clock import Clock

    # Aufrufen
    # self.update_graph(HistoryProvider.get_week("temp_in_avg"))

class HistoryScreen(Screen):
    state = ObjectProperty(None)
    current_date = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_date = datetime.now()

    def on_kv_post(self, base_widget):
        self.plot = LinePlot(color=[0.2, 0.7, 1, 1], line_width=2)
        self.ids.temp_graph.add_plot(self.plot)    

    def on_enter(self):
        self.show_day()
        #self.prev_day()


    def show_day(self):
        data = HistoryProvider.get_day("temp_in_avg", self.current_date)
        #self.update_graph(data, hours=24)
        self.update_day_graph(data)

    def prev_day(self):
        self.current_date = self.current_date - timedelta(days=0.5)
        if self.current_date < datetime.now() - timedelta(days=3):
            self.current_date = datetime.now() - timedelta(days=2.5)
        self.show_day()

    def next_day(self):
        self.current_date = self.current_date + timedelta(days=1)
        if self.current_date > datetime.now():
            self.current_date = datetime.now()
        self.show_day()


    def show_week(self):
        data = HistoryProvider.get_week("temp_in_avg")
        #self.update_graph(data, hours=7 * 24)
        self.update_week_graph(data)

    def show_month(self):
        data = HistoryProvider.get_month("temp_in_avg")
        #self.update_graph(data, hours=30 * 24)
        self.update_month_graph(data)

    def clear_graph(self):
        self.plot.points = []


    def update_day_graph(self, data):
        graph = self.ids.temp_graph

        if not hasattr(self, "plot"):
            self.plot = LinePlot(color=[1, 0, 0, 1], line_width=2)
            graph.add_plot(self.plot)
        else:
            # Vorherige Punkte löschen
            self.plot.points = []

        if not data:
            return

        day_start = int(
            self.current_date.replace(
                hour=0, minute=0, second=0, microsecond=0
            ).timestamp()
        )

        points, values = [], []

        for ts, value in data:
            if value is None:
                continue
            x = (ts - day_start) / 3600  # Stunden seit Tagesbeginn
            points.append((x, value))
            values.append(value)

        if not values:
            self.clear_graph()
            return

        graph.xmin = 0
        graph.xmax = 24
        graph.x_ticks_major = 2
        graph.xlabel = "Zeit (Stunden)"
        graph.ylabel = "Temperatur (°C)"

        self.apply_y_axis(graph, values)
        self.plot.points = points


    def update_week_graph(self, data):
        graph = self.ids.temp_graph

        if not data:
            self.clear_graph()
            return

        start_ts = data[0][0]

        points, values = [], []

        for ts, value in data:
            if value is None:
                continue
            x = (ts - start_ts) / 86400  # Tage seit Start
            points.append((x, value))
            values.append(value)

        graph.xmin = 0
        graph.xmax = 7
        graph.x_ticks_major = 1
        graph.xlabel = "Zeit (Tage)"
        graph.ylabel = "Temperatur (°C)"

        self.apply_y_axis(graph, values)
        self.plot.points = points


    def update_month_graph(self, data):
        graph = self.ids.temp_graph

        if not data:
            self.clear_graph()
            return

        start_ts = data[0][0]

        points, values = [], []

        for ts, value in data:
            if value is None:
                continue
            x = (ts - start_ts) / 86400  # Tage seit Start
            points.append((x, value))
            values.append(value)

        graph.xmin = 0
        graph.xmax = 30
        graph.x_ticks_major = 5
        graph.xlabel = "Zeit (Tage)"
        graph.ylabel = "Temperatur (°C)"

        self.apply_y_axis(graph, values)
        self.plot.points = points


    def apply_y_axis(self, graph, values):
        min_y = min(values)
        max_y = max(values)

        graph.ymin = int(min_y // 5) * 5 - 5
        graph.ymax = int(max_y // 5 + 1) * 5 + 5
        graph.y_ticks_major = 5

