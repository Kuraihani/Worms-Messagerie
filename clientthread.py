from socket import socket
import threading 
import re 
import time
import json
import datetime

class ClientListener(threading.Thread):

    def __init__(self, server, socket, address):
        super(ClientListener, self).__init__()
        self.server= server
        self.socket= socket
        self.address= address
        self.listening= True
        self.username= "No username"

        
    def run(self):
        while self.listening:
            data= ""
            try:
                data = self.socket.recv(1024).decode('UTF-8')
            except Exception as e:
                print("Unable to receive data: {}".format(e))
            self.handle_msg(data)
            time.sleep(0.1)
        print("Ending client thread for", self.address)

    def quit(self):
        self.listening = False
        self.socket.close()
        self.server.remove_socket(self.socket)
        self.server.echo("{0} has quit\n".format(self.username))

    def handle_msg(self, data):
        print(self.address, "sent :", data)
        username_result = re.search('^USERNAME (.*)$', data)
        if username_result:
            self.username = username_result.group(1)
            self.server.echo("{0} has joined.\n".format(self.username))
        elif data == "QUIT":
            self.quit()
        elif data == "":
            self.quit()
        else:

            #ECRITURE MESSAGERIE
            self.server.echo(data)
            with open('message.txt') as json_file:
                self.data_message = json.load(json_file)

            if(len(self.data_message['message']) > 6):
                del self.data_message['message'][1]
        
            self.data_message['message'].append({
                'isGame':False,
                'text_message': data
            })

            with open('message.txt', 'w') as outfile:
                json.dump(self.data_message, outfile)
