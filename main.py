from kivy.config import Config
Config.set('graphics', 'borderless', 1)

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore

from kivymd.app import MDApp
from kivymd.uix.button import MDExtendedFabButton
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarSupportingText,MDSnackbarButtonContainer
from kivymd.uix.snackbar import MDSnackbarActionButtonText,MDSnackbarActionButton,MDSnackbarCloseButton

import trial
from threading import Thread

from utils.connection import Server, Client

class MyMDExtendedButton(MDExtendedFabButton, HoverBehavior):
    pass

class UI(MDApp):
    def build(self):
        self.server = None
        self.server_state = None
        self.client = None
        self.theme_cls.theme_style = "Dark"
        self.ssid = trial.find_ssid()
        self.ip_address = trial.find_ip_address()
        self.storage_manager = JsonStore(r"storage\data.json")
        return Builder.load_file(r"design\design.kv")

    def start_server(self, ip="0.0.0.0", port=5000, *args):
        port = int(port )
        if self.server==None:
            self.server = Server(host_ip=ip, host_port=port)
            Thread(target=self.server.start_listening).start()
            self.server_state = "Running"
        else:
            self.info_pass("Server is already up and running")
    def stop_server(self):
        if self.server==None:
            self.info_pass("Server not yet started")
        else:
            Thread(target=self.server.stop_listening).start()
            self.server = None
            self.server_state = None
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