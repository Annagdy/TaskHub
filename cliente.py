import socket 

class Cliente:
    
    def __init__(self):
        self.ip = ''
        self.port = 8087
        self.address = (self.ip, self.port)
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente_socket.connect(self.address)

    def enviar(self, mensagem):
        self.cliente_socket.send(mensagem.encode())
        recebeu = self.cliente_socket.recv(1024).decode()
        verificador = recebeu.split(",")
        print(verificador)
        if verificador[0] == '-1':
            self.cliente_socket.close()
        return recebeu