from kivy.app import App
from kivy.uix.floatlayout import *
from kivy.uix.boxlayout import *
from kivy.properties import *
from kivy.uix.slider import *
from kivy.graphics import *
from kivy.uix.button import *

import os

class change_styleApp(App):

    def __init__(self):
        App.__init__(self)
        
    def build(self):
        return MainWindow()

class MainWindow(BoxLayout):

    def __init__(self, **kwargs):

        super(MainWindow, self).__init__()

class NewButton(Button):
    pass    
        
if __name__ == '__main__':
    
    change_styleApp().run()
