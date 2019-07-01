import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, NoTransition, SwapTransition
from kivy.config import Config
from kivy.core.window import Window
import os
from time import sleep

Config.set('graphics', 'width', '540')  # default 1080
Config.set('graphics', 'height', '960')  # default 1920
Config.set('graphics', 'resizable', False)

class HomePage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.row_force_default = True
        self.row_default_height = 40

        self.add_widget(Label(text='Calendar Transfer', font_size=36, halign='left', color=lightGrey,  size_hint_x=None, width=300))
        self.add_widget(Label(text=''))

        self.add_widget(Label(text='Apple & Google supported', font_size=24, halign='left', color=dimGrey,  size_hint_x=None, width=300))
        self.add_widget(Label(text=''))

        self.AppleSetting = Button(text='Apple settings')
        self.AppleSetting.bind(on_press=self.AppleSetting_Button)
        self.add_widget(self.AppleSetting)

    def AppleSetting_Button(self, instance):
        print("Test")

        CalTrans.screen_manager.transition = NoTransition()
        CalTrans.screen_manager.current = "Home"


class CalTransApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.home_page = HomePage()
        screen = Screen(name='Home')
        screen.add_widget(self.home_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == "__main__":
    kivy.require("1.10.1")

    # colors:
    dimGrey = (0.337, 0.341, 0.4, 1)
    lightGrey = (0.788, 0.788, 0.851, 1)
    midnightBlue = (0.141, 0.067, 0.255, 1)
    black = (0.075, 0, 0.173, 1)

    Window.clearcolor = black

    CalTrans = CalTransApp()
    CalTrans.run()
