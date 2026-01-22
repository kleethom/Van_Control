from kivy.config import Config

def setup():
    Config.set("graphics", "fullscreen", "auto")
    Config.set("graphics", "borderless", "1")
    Config.set("graphics", "resizable", "0")
    Config.set("kivy", "keyboard_mode", "systemanddock")
    Config.set("input", "mouse", "mouse,disable_multitouch")