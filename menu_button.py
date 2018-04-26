from kivy.uix.button import Button
from kivy.lang import Builder

Builder.load_file('menu_button.kv')


class MenuButton(Button):

    def __init__(self, **kwargs):
        Button.__init__(self, **kwargs)


if __name__ == "__main__":

    from kivy.app import App

    class TestApp(App):
        def build(self):
            return MenuButton()

    TestApp().run()