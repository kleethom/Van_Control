from kivy.uix.widget import Widget
from kivy.graphics import Line, Color

class LineChart(Widget):

    def set_data(self, points):
        self.canvas.clear()
        if not points:
            return

        xs = [p[0] for p in points]
        ys = [p[1] for p in points if p[1] is not None]

        if not ys:
            return

        min_y = min(ys)
        max_y = max(ys)

        with self.canvas:
            Color(0.2, 0.7, 1)
            Line(points=self._normalize(xs, ys, min_y, max_y), width=2)

    def _normalize(self, xs, ys, min_y, max_y):
        w, h = self.size
        min_x, max_x = min(xs), max(xs)

        points = []
        for x, y in zip(xs, ys):
            nx = (x - min_x) / (max_x - min_x) * w
            ny = (y - min_y) / (max_y - min_y) * h
            points.extend([nx, ny])
        return points