import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, NoTransition, SwapTransition
kivy.config.Config.set('graphics','resizable', False)
from kivy.core.window import Window
import os
from time import sleep
kivy.require("1.10.1")


Window.size = (1080/3, 1920/3)

class HomePage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.row_force_default = True
        self.row_default_height = 50

        self.add_widget(Label(text='Calendar Transfer', font_size=36, halign='left', color=lightGrey,  size_hint_x=None, width=300))
        self.add_widget(Label(text=''))

        self.add_widget(Label(text='Apple & Google supported', font_size=24, halign='left', color=dimGrey,  size_hint_x=None, width=300, size_hint_y=None, height=80))
        self.add_widget(Label(text=''))

        self.add_widget(Label(text="Apple settings", halign='left', font_size=26, color=lightGrey, size_hint_x=None, width=180))
        self.add_widget(Label(text=''))

        self.AppleSetting = Button(text='Change Apple settings', halign='left', size_hint_x=-50, width=50)
        self.AppleSetting.bind(on_press=self.AppleSetting_Button)
        self.add_widget(self.AppleSetting)
        self.add_widget(Label(text=''))

        self.add_widget(Label(text="Google settings", halign='left', font_size=26, color=lightGrey, size_hint_x=None, width=180))
        self.add_widget(Label(text=''))

        self.GoogleSetting = Button(text='Change Google settings')
        self.GoogleSetting.bind(on_press=self.GoogleSetting_Button)
        self.add_widget(self.GoogleSetting)
        self.add_widget(Label(text=''))

    def AppleSetting_Button(self, instance):
        print("Test")

        CalTrans.screen_manager.transition = NoTransition()
        CalTrans.screen_manager.current = "AppleSettings"

    def GoogleSetting_Button(self, instance):
        print("Test")

        CalTrans.screen_manager.transition = NoTransition()
        CalTrans.screen_manager.current = "Home"


class AppleSettingPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1

        self.add_widget((Label(text='Apple Settings', font_size=36, halign='left', valign='top', color=lightGrey,  size_hint_x=None, width=250, size_hint_y=None, height=-50)))
        self.add_widget(Label(text=''))

        self.add_widget(TextInput(text='place Apple key here', multiline=False, size_hint_y=None, height=30))
        self.AppleConTest = Button(text='Add Apple Key', halign='left', height=-50)
        self.AppleConTest.bind(on_press=self.AppleConTest_Button)
        self.add_widget(self.AppleConTest)
        AppleKey = 'none'
        self.add_widget(Label(text=str('Current apple key:\t'+AppleKey), color=dimGrey))

        self.AppleConTest = Button(text='Test Apple connection', halign='left', height=-50, width=50)
        self.AppleConTest.bind(on_press=self.AppleConTest_Button)
        self.add_widget(self.AppleConTest)
        self.add_widget(Label(text=''))

        self.add_widget(Label(text='Place holder', halign='left', valign='middle'))

    def AppleConTest_Button(self, instance):
        print("Testing connection")


class CalTransApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.home_page = HomePage()
        screen = Screen(name='Home')
        screen.add_widget(self.home_page)
        self.screen_manager.add_widget(screen)

        self.AppleSetting_page = AppleSettingPage()
        screen = Screen(name='AppleSettings')
        screen.add_widget(self.AppleSetting_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == "__main__":

    # colors:
    dimGrey = (0.337, 0.341, 0.4, 1)
    lightGrey = (0.788, 0.788, 0.851, 1)
    midnightBlue = (0.141, 0.067, 0.255, 1)
    black = (0.075, 0, 0.173, 1)

    Window.clearcolor = black  # Sets background to black

    CalTrans = CalTransApp()
    CalTrans.run()
