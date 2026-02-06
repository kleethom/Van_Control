from gui.data.history_provider import HistoryProvider
from gui.charts.line_chart import LineChart
from kivy.uix.boxlayout import BoxLayout

class HistoryView(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chart = LineChart()
        self.add_widget(self.chart)

        data = HistoryProvider.get_day("temp_in_avg")
        self.chart.set_data(data)