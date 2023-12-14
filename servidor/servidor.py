import socket, threading
from banco_de_dados import Banco
import datetime
import json

#fazer de acordo com o taskhub

def tratar_mensagem(mensagem):
    l = mensagem.split("-")
    envia = ''
    if l[0] == '-1':
        envia = "-1"
    elif l[0] == '-2':
        envia = "-2"
    elif l[0] == '0': 
        username = l[1]
        senha = l[2]
        if banco.logar_usuario(username, senha):
            banco.obter_nome_usuario_logado()
            envia = "1"
            print(f'{username} entrou no TaskHub!')
        else:
            envia = "0"
    elif l[0] == '1':
        username = l[1]
        email = l[2]
        senha = l[3]
        if banco.cadastrar_usuario(username, email, senha):
            envia = '1'
            print(f'{username} agora faz parte do TaskHub.')
        else:
            envia = '0'
    elif l[0] == '2':
        #devolve o nome do usuario logado
        if banco.obter_nome_usuario_logado():
            envia = banco.obter_nome_usuario_logado()
        else:
            envia = '0'
    else:
        envia = "comando invalido"
    return envia
        
        


class ClientThread(threading.Thread):
   
    def __init__(self, connection):
    
        super().__init__()
        self.con = connection
    
    def run(self):

        while True:
            recebe = self.con.recv(1024)
            enviar = tratar_mensagem(recebe.decode())
            if enviar == "-1":
                self.con.send(enviar.encode())
                break
            else:
                self.con.send(enviar.encode())



if __name__ == "__main__":
    host = '0.0.0.0'
    port = 8087
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((host,port))
    banco = Banco()

    while True:
        server_socket.listen(10)
        print("esperando cliente...")
        con, cliente = server_socket.accept()
        print("cliente aceito...")
        sinc = threading.Lock()
        newThread = ClientThread(con)
        newThread.start()