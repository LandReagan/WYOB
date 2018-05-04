from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

Builder.load_file('menu.kv')


class Menu(BoxLayout):

    def __init__(self, parent, **kwargs):
        BoxLayout.__init__(self, **kwargs)
        self.gui = parent

    def onLogin(self):
        pass

    def onUpdate(self):
        self.gui.update()
