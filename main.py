from kivy.config import Config
Config.set('graphics', 'borderless', 1)

from kivy.lang import Builder
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.button import MDExtendedFabButton
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarSupportingText,MDSnackbarButtonContainer
from kivymd.uix.snackbar import MDSnackbarActionButtonText,MDSnackbarActionButton,MDSnackbarCloseButton

import trial

class MyMDExtendedButton(MDExtendedFabButton, HoverBehavior):
    pass

class UI(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.ssid = trial.find_ssid()
        self.ip_address = trial.find_ip_address()
        return Builder.load_file(r"design\design.kv")

    def refresh(self, *args):
        self.ssid = trial.find_ssid()
        self.ip_address = trial.find_ip_address()
    def info_pass(self,text, *args):
        MDSnackbar(
            MDSnackbarSupportingText(
                text=text,
            ),
            auto_dismiss=True,
            y=100,
            orientation="horizontal",
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5,
        ).open()


if __name__ == '__main__' :
    UI().run()