import kivy

from App_Code import Calendar_transfer as CT
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, NoTransition, SwapTransition
kivy.config.Config.set('graphics','resizable', False)
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.clock import Clock
import os
from time import sleep

kivy.require("1.10.1")


Window.size = (1080/3, 1920/3)

class errorPopup(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols=1

    def mainError(self):
        content = GridLayout(cols=1)

        errorLabel = Label(text="Something went wrong")
        errorButton = Button(text='Close')

        content.add_widget(errorLabel)
        content.add_widget(errorButton)

        popup = Popup(title='Error',
                      content=content,
                      size_hint=(None, None), size=(200, 150),
                      auto_dismiss=False)

        popup.open()
        errorButton.bind(on_press=popup.dismiss)


class HomePage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.row_force_default = True
        self.row_default_height = 50

        self.add_widget(Label(text='Calendar Transfer', font_size=36, halign='left', color=lightGrey,  size_hint_x=None, width=300))
        self.add_widget(Label(text=''))

        self.add_widget(Label(text='Apple & Google supported', font_size=24, halign='left', color=dimGrey,
                              size_hint=[None,None] , width=300, height=80))
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
    appleKey = StringProperty()
    appleKey = ""

    def __init__(self, appleKey="", **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        appleKey = "No key"


        file = open("Data/AppleToken.txt", "r")
        appleKey = file.readline()
        print(appleKey)
        if appleKey == "":
            appleKey = "No key"

        self.add_widget((Label(text='Apple Settings', font_size=36, halign='left', valign='top', color=lightGrey,
                               size_hint=[None, None], width=250, height=-50)))
        self.add_widget(Label(text=''))

        #self.add_widget((Label(text='Place your apple key here')))
        #self.add_widget(TextInput(multiline=False, size_hint_y=None, height=30, font_size=11))
        self.setAppleCon = Button(text='Set Apple Key', halign='left', size_hint=[None,None], height=30, width=200)
        self.setAppleCon.bind(on_press=self.setAppleCon_Button)
        self.add_widget(self.setAppleCon)


        self.add_widget(Label(text=str('Current apple key:'), color=lightGrey, halign='auto', size_hint=[None, None], width=200))
        self.add_widget(TextInput(text="testing"))

        self.AppleConTest = Button(text='Test Apple connection', halign='left', size_hint=[None, None], height=30, width=200)
        self.AppleConTest.bind(on_press=self.AppleConTest_Button)
        self.AppleConTest.disabled = True
        self.add_widget(self.AppleConTest)
        self.add_widget(Label(text=''))

        self.add_widget(Label(text='Place holder', halign='left', valign='middle'))

        self.Home = Button(text='Home', size_hint=[None, None], height=50, width=350)
        self.Home.bind(on_press=self.Home_Button)
        self.add_widget(self.Home)


    def Home_Button(self, instance):
        CalTrans.screen_manager.transition = NoTransition()
        CalTrans.screen_manager.current = "Home"

    def setAppleCon_Button(self, instance):
        box = GridLayout(cols=2)
        popupLabel = Label(text="Place your key here")
        ph = Label(text="")
        ph1 = Label(text="")
        popupText = TextInput(multiline=False, font_size=11, width=170, size_hint_x=None)
        buttonBox = GridLayout(cols=2)
        popupSetButton = Button(text="Set Key", halign="left", size_hint_x=None, width= 85)
        popupCloseButton = Button(text="Close", halign="left", size_hint_x=None, width= 85)

        box.add_widget(popupLabel)
        box.add_widget(ph)

        box.add_widget(popupText)
        box.add_widget(ph1)

        buttonBox.add_widget(popupSetButton)
        buttonBox.add_widget(popupCloseButton)
        box.add_widget(buttonBox)

        popup = Popup(title="Add Apple key", content=box, size_hint=[None, None], size=(200, 150), auto_dismiss=False)
        popup.open()

        def writeKey(self):
            key = str(popupText.text)
            file = open("Data/AppleToken.txt", "w")
            file.write(key)
            print(key)


        popupSetButton.bind(on_press=writeKey)

       # popupSetButton.bind(on_press=CT.appleAPISetup(setKey))                   # Writes key to 'Apple Token' File)
        popupSetButton.bind(on_press=popup.dismiss)

        popupCloseButton.bind(on_press=popup.dismiss)


    def AppleConTest_Button(self, instance):
        print("Testing connection")

        box = GridLayout()
        box.cols=1

        #CT.AppleConCheck()
        popupLabel = Label(text='Hello world')
        popupButton = Button(text='Close me!')

        box.add_widget(popupLabel)
        box.add_widget(popupButton)

        popup = Popup(title='Test popup',
                      content=box,
                      size_hint=(None, None), size=(200, 150),
                      auto_dismiss=False)

        popup.open()
        popupButton.bind(on_press=popup.dismiss)
    key = setAppleCon_Button


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
