# WYOB.py

from kivy.app import App

from gui import GUI


class WYOB(App):

    def build(self):
        return GUI()


if __name__ == '__main__':
    WYOB().run()
