'''
Python == 3.12.2
Date == 03/09/2024
'''
import sys
import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init
import subprocess

class Server:
    def __init__(self, host_ip, host_port=5000, queue=5):
        self.ip = host_ip
        self.port = host_port

        self.__client_sockets_list = set()
        self.__socket_object = socket.socket()
        self.__socket_object.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket_object.bind((self.ip, self.port))
        self.__socket_object.listen(queue)
        self.__listen = False
        self.__separator = "<SEP>"

    def __show_message(self,ip="", welcome=False, disconnected=False):
        if welcome:
            print(f"[*] Listening as {self.ip} on port {self.port}")
        elif disconnected:
            print(f"--)     {ip} disconnected")
        else:
            print(f"-->     {ip} connected")
    
    def start_listening(self):
        self.__listen = True
        self.__show_message(welcome=True)
        self.__accept_clients_connection()

    def stop_listening(self):
        print(f"[*] Shuting Down Connection")
        self.__listen = False
        self.__socket_object.close()
        sys.exit()


    
    def __listen_for_clients_message(self, client_socket,ip):
        ip = ip
        while self.__listen:
            if self.__socket_object == None:
                break
            try:
                msg = client_socket.recv(1024).decode()
            except Exception as e:
                self.__client_sockets_list.remove(client_socket)
                self.__show_message(ip=ip,disconnected=True)
            else:
                msg = msg.replace(self.__separator, ":")
                if msg.split(":")[1] == "`249942":
                    client_socket.send("`249942".encode())
                    client_socket.close()
                    self.__client_sockets_list.remove(client_socket)
                    self.__show_message(ip=ip,disconnected=True)
                    break
            

            for client_socket_i in self.__client_sockets_list:
                client_socket_i.send(msg.encode())
    
    def __accept_clients_connection(self):
        while self.__listen:
            try:
                client_socket, client_address = self.__socket_object.accept()
                self.__show_message(ip=client_address)
                self.__client_sockets_list.add(client_socket)
                self.__client_thread = Thread(target=self.__listen_for_clients_message,args=(client_socket, client_address,), daemon=True)
                self.__client_thread.start()
            except:
                pass

class Client:
    def __init__(self, server_ip, server_port, name):
        self.connectiont_ip = server_ip
        self.connection_port = server_port
        self.__separator = "<SEP>"
        self.__connect_server = False
        
        self.__name = name
        init()
        self.__colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
            Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
            Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
            Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
        ]
        self.__text_color = random.choice(self.__colors)
    
    def connect(self):
        try:
            self.__socket_object = socket.socket()
            self.__socket_object.connect((self.connectiont_ip, self.connection_port))
            self.__connect_server = True
            t = Thread(target=self.__listen_to_server, daemon=True)
            t.start()
            print("[+] Connected.")
        except Exception as e:
            print("1/ / Connection Error! / / ", e)
    
    def disconnect(self):
        try:
            self.__connect_server = False
            self.__socket_object.close()
        except:
            print("2/ / Couldn't Disconnect Properly! / / ")

    def __listen_to_server(self):
        while self.__connect_server:
            try:
                message = self.__socket_object.recv(1024).decode()
                if message == "`249942":
                    print("[-] Disconnected.")
                    break
                print("\n" + message)
            except:
                print("3 Error on Thread")
    
    def get_message_from_console(self):
        while self.__listen_to_server:
            message = input("--->")
            if message.lower() == 'q':
                key = "`249942"
                message = f"{self.__text_color} {self.__name}{self.__separator}{key}"
                self.__socket_object.send(message.encode())
                self.disconnect()
                exit()
                break
            self.__broadcast_message(message=message)

    def __broadcast_message(self, message=""):
        __message_to_send = message
        __date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        __message_to_send = f"{self.__text_color}[{__date_now}] {self.__name}{self.__separator}{__message_to_send}{Fore.RESET}"
        try:
            self.__socket_object.send(__message_to_send.encode())
        except:
            print(" 4/ / Connection Error! / /")      

def find_ip_address():
    try:
        c = socket.gethostbyname(socket.gethostname())
    except:
        c = "Not Connected"
    return c


def find_ssid():
    interface = subprocess.check_output(['netsh', 'WLAN', 'show', 'interfaces'])
    data = interface.decode('utf-8')
    try:
        ssid = data[data.find("SSID"):data.find("BSSID")].split(":")[1].strip()
    except:
        ssid = "Not Connected"
    return ssid


'''
if __name__ == "__main__":
    
    #server = Server("0.0.0.0")
    #Thread(target=server.start_listening).start()
    #Thread(target=server.stop_listening).start()
    
    #client = Client("127.0.0.1", 5002, "Nithish")
    #client.connect()
    #client.get_message_from_console()
'''
