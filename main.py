import config.config
config.config.setup()

from kivy.core.window import Window
Window.show_cursor = False


from core.app import VanControlApp

def main():
    app = VanControlApp()
    app.start()

if __name__ == "__main__":
    main()