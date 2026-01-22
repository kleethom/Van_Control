from kivy.event import EventDispatcher
from kivy.properties import NumericProperty


class SystemState(EventDispatcher):
    temperature_inside = NumericProperty(0.0)
    humidity_inside = NumericProperty(0.0)