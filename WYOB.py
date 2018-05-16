# WYOB.py

from os.path import join

from kivy.app import App

from gui import GUI
import config


class WYOB(App):

    def build(self):
        config.root_directory = getattr(self, 'user_data_dir')
        config.data_file_path = join(config.root_directory, 'data.json')
        return GUI()
