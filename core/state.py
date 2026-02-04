from kivy.event import EventDispatcher
from kivy.properties import NumericProperty


class SystemState(EventDispatcher):
    temperature_inside = NumericProperty(0.0)
    humidity_inside = NumericProperty(0.0)

    temperature_outside = NumericProperty(0.0)
    humidity_outside = NumericProperty(0.0)

    pressure = NumericProperty(0.0)
    altitude = NumericProperty(0.0)

    tilt_x = NumericProperty(0.0)
    tilt_y = NumericProperty(0.0)