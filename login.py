from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder

Builder.load_file("login.kv")


class Login(GridLayout):

    def __init__(self, **kwargs):
        GridLayout.__init__(self, **kwargs)
