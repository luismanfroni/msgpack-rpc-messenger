import msgpackrpc
import time
from os import system, name 
import sys
import threading

def run_in_thread(fn):
    def run(*k, **kw):
        t = threading.Thread(target=fn, args=k, kwargs=kw)
        t.start()
        return t
    return run

def clearScreen():
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

class Messageria:
    name = None
    address = None
    lobby = []
    server = None
    messages = []

    @run_in_thread
    def startServer():
        print(f'Host em: { Messageria.address }')
        serverObj = MsgServer()
        Messageria.server = msgpackrpc.Server(serverObj)
        Messageria.server.listen(msgpackrpc.Address(Messageria.address[0], 
            Messageria.address[1]))
        Messageria.lobby.append(Messageria.address)
        Messageria.server.start()

    @run_in_thread
    def sendMessage(message):
        for address in Messageria.lobby:
            try:
                client = msgpackrpc.Client(msgpackrpc.Address(address[0], address[1]))
                client.call('receiveMessage', (Messageria.name, message))
            except Exception as e:
                Messageria.lobby.remove(address)

class MsgServer(object):
    def connect(self, address):
        client = msgpackrpc.Client(msgpackrpc.Address(address[0], address[1]))
        if client.call('connectSuccess'):
            Messageria.lobby.append((address[0], address[1]))
            return True
        return False

    def connectSuccess(self):
        return True

    def getLobby(self):
        return Messageria.lobby

    def receiveMessage(self, message):
        if type(message[0]) == bytes or type(message[1]) == bytes:
            message[0] = message[0].decode("utf-8")
            message[1] = message[1].decode("utf-8")
        Messageria.messages.append(message)
        refreshScreen()
        return True

def refreshScreen():
    clearScreen()
    for message in Messageria.messages:
        print(f"({ message[0] }): { message[1] }")

    print("Insira uma mensagem e pressione enter para enviar:")

def conectar():
    endereco = informarEndereco(False)
    client = msgpackrpc.Client(msgpackrpc.Address(endereco[0], endereco[1]))
    Messageria.lobby = client.call('connect', Messageria.address)
    Messageria.lobby = client.call('getLobby')
    clearScreen()
    messengerLoop()

def messengerLoop():
    while True:
        print("Insira uma mensagem e pressione enter para enviar:")
        message = input("")
        Messageria.sendMessage(message)

def informarEndereco(my):
    try:
        message = "Informe seu ip (10.199.36.56): "
        if not my:
            message = "Informe o ip para conectar: "
        ip = input(message)
        if ip.strip() == '':
            ip = '10.199.36.56'

        message = "Informe sua porta (20000): "
        if not my:
            message = "Informe a porta para conectar: "
        port = input(message)
        if port.strip() == '':
            port = 20000
        else:
            port = int(port)
        
        if my:
            Messageria.address = [ip, port]
            Messageria.startServer()
        else:
            client = msgpackrpc.Client(msgpackrpc.Address(ip, port))
            client.call('connectSuccess')

        return (ip, port)
    except:
        #clearScreen()
        print("IP/Porta incorreto")
        return informarEndereco(my)


def main():
    Messageria.name = input("Informe seu nome: ")
    
    Messageria.address = informarEndereco(True)
    
    aguardar = 'B'
    while aguardar.upper() not in 'CAS' or aguardar.strip() == '':
        aguardar = input("Escolha uma opcao ([C]onectar, [A]guardar, [S]air): ")

    if aguardar.upper() == 'C':
        conectar()
    elif aguardar.upper() == 'A':
        clearScreen()
        messengerLoop()

if __name__ == '__main__':
    main()