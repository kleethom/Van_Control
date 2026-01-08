from kivy.config import Config
Config.set("graphics", "fullscreen", "auto")
Config.set("graphics", "borderless", "1")
Config.set("graphics", "resizable", "0")
Config.set("kivy", "keyboard_mode", "systemanddock")
Config.set("input", "mouse", "mouse,disable_multitouch")

from kivy.core.window import Window
Window.show_cursor = False


from core.app import VanControlApp

def main():
    app = VanControlApp()
    app.start()

if __name__ == "__main__":
    main()