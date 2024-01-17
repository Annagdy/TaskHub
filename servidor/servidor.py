import socket
import threading
from banco_de_dados import Banco
import datetime
import json

# Fazer de acordo com o TaskHub

def tratar_mensagem(mensagem):
    """
    Processa a mensagem recebida e retorna uma resposta.

    A função tratar_mensagem processa a mensagem recebida do cliente e retorna uma resposta.
    Ela analisa o primeiro elemento da lista resultante para determinar qual ação realizar.
    A resposta é então retornada para ser enviada de volta ao cliente.

    Parameters
    ----------
    mensagem : str
        A mensagem recebida do cliente.

    Returns
    -------
    envia : str
        A resposta em string para ser enviada de volta ao cliente.
    """

    l = mensagem.split("-")
    envia = ''

    # Verifica o tipo de comando e executa a ação correspondente
    if l[0] == '-1':
        envia = "-1"
    elif l[0] == '-2':
        envia = "-2"
    elif l[0] == '0':
        username = l[1]
        senha = l[2]
        # Verifica se o usuário pode fazer login
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
        # Cadastra um novo usuário
        if banco.cadastrar_usuario(username, email, senha):
            envia = '1'
            print(f'{username} agora faz parte do TaskHub.')
        else:
            envia = '0'
    elif l[0] == '2':
        # Devolve o nome do usuário logado
        if banco.obter_nome_usuario_logado():
            envia = banco.obter_nome_usuario_logado()
        else:
            envia = '0'
    elif l[0] == '3':
        #verifica se o usuário existe
        if banco.usuarioExiste(l[1]):
            envia = '1'
        else:
            envia = '0'
    else:
        envia = "Comando inválido"

    return envia

class ClientThread(threading.Thread):
    """
    Classe que representa uma thread para lidar com a comunicação com um cliente.

    ...

    Attributes
    ----------
    connection : socket
        O objeto de conexão com o cliente.

    Methods
    -------
    __init__(self, connection)
        Construtor da classe. Inicializa o objeto de conexão com o cliente.

    run(self)
        Executa a thread do cliente.
    """

    def __init__(self, connection):
        """
        Parameters
        ----------
        connection : socket
            O objeto de conexão com o cliente.
        """

        super().__init__()
        self.con = connection
    
    def run(self):
        """
        Executa a thread do cliente.

        Este método é executado quando a thread do cliente é iniciada. Ele contém um loop infinito que recebe
        mensagens do cliente, processa essas mensagens utilizando a função `tratar_mensagem`, e envia a resposta
        de volta ao cliente.
        """

        while True:
            recebe = self.con.recv(1024)
            enviar = tratar_mensagem(recebe.decode())
            
            # Verifica se há uma instrução especial de encerramento
            if enviar == "-1":
                self.con.send(enviar.encode())
                break
            else:
                self.con.send(enviar.encode())

if __name__ == "__main__":
    host = '0.0.0.0'
    port = 8087
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    banco = Banco()

    while True:
        server_socket.listen(10)
        print("Esperando cliente...")
        con, cliente = server_socket.accept()
        print("Cliente aceito...")
        sinc = threading.Lock()
        newThread = ClientThread(con)
        newThread.start()
