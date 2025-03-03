from kivy.config import Config
Config.set('graphics', 'borderless', 1)

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.properties import StringProperty, BooleanProperty

from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.button import MDExtendedFabButton
from kivymd.uix.list import (
    MDList,
    MDListItem,
    MDListItemHeadlineText,
    MDListItemLeadingIcon,
)
from kivymd.uix.snackbar import (
    MDSnackbar,
    MDSnackbarSupportingText,
    MDSnackbarButtonContainer,
    MDSnackbarActionButtonText,
    MDSnackbarActionButton,
    MDSnackbarCloseButton
)
from threading import Thread
import ipaddress
import socket

from utils.connection import Server, Client, find_ip_address, find_ssid

class MyMDExtendedButton(MDExtendedFabButton, HoverBehavior):
    pass

class MessageCard(MDCard):
    message = StringProperty()
    is_user = BooleanProperty()

    def __init__(self, message, is_user, **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.is_user = is_user

class UI(MDApp):
    def build(self):
        self.server = None
        self.server_state = None
        self.client = None
        self.port = 5000
        self.server_list = []
        self.theme_cls.theme_style = "Dark"
        self.ssid = find_ssid()
        self.ip_address = find_ip_address()
        self.storage_manager = JsonStore(r"storage\data.json")
        return Builder.load_file(r"design\design.kv")

    def start_server(self, ip="0.0.0.0", port="5000", *args):
        port = int(port)
        if self.server is None:
            try:
                self.server = Server(host_ip=ip, host_port=port)
                Thread(target=self.server.start_listening).start()
                self.server_state = "Running"
                self.info_pass("Server is up and running")
            except Exception as e:
                self.info_pass(f"Error: {e}")
        else:
            self.info_pass("Server is already up and running")

    def stop_server(self):
        if self.server==None:
            self.info_pass("Server not yet started")
        else:
            try:
                Thread(target=self.server.stop_listening).start()
                self.server = None
                self.server_state = None
                self.info_pass("Server is down")
            except Exception as e:
                self.info_pass(f"Failed to stop server: {e}")
    def add_server_to_list(self, ip_str):
        """Add a server to the GUI list"""
        def add_item(dt):
            server_item = MDListItem(
                MDListItemLeadingIcon(
                    icon="server-network",
                ),
                MDListItemHeadlineText(
                    text=f"Server at {ip_str}",
                ),
                on_release=lambda x: self.connect_to_server(ip_str)
            )
            self.root.ids.server_list.add_widget(server_item)
            print(f"Added server to list:{ip_str}")
        Clock.schedule_once(add_item)
    
    def connect_to_server(self, ip):
        """Handle server connection"""
        try:
            self.client = Client(ip, self.port, "User")  # You might want to get username from settings
            self.client.connect()
            self.info_pass(f"Connected to server at {ip}")
            self.root.current = "chat_screen"  # Switch to chat screen when implemented
        except Exception as e:
            self.info_pass(f"Connection failed: {e}")

    def send_message(self):
        message_entry = self.root.ids.message_entry
        message = message_entry.text.strip()
        if message:
            chat_area = self.root.ids.chat_area
            m = MessageCard(message=message, is_user=True)
            chat_area.add_widget(m)
            message_entry.text = ""

    def refresh(self, *args):
        self.ssid = find_ssid()
        self.ip_address = find_ip_address()

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

    def search(self):
        self.server_list = []
        self.root.ids.server_list.clear_widgets()
        self.root.ids.scan_progress.value = 0
        Thread(target=self.find_server_on_lan, args=[self.port]).start()
        
    def find_server_on_lan(self,port,timeout=0.1):
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        ip_network = ipaddress.ip_network(local_ip + '/24', strict=False)

        value = 1
        for ip in ip_network.hosts():
            ip_str = str(ip)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                try:
                    s.connect((ip_str, port))
                    s.send("asdasd:`249942".encode())
                    print(f"Server found at {ip_str}")
                    self.server_list.append(ip_str)
                    Clock.schedule_once(lambda dt, ip_str=ip_str: self.add_server_to_list(ip_str))
                except (socket.timeout, ConnectionRefusedError):
                    pass
                finally:
                    value+=1
                    self.root.ids.scan_progress.value = int((value/255) * 100) 
    
if __name__ == '__main__' :
    UI().run()