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
    # Command '3' - cadastrar_tarefa
    elif l[0] == '3':
        try:
            if len(l) >= 8:
                titulo = l[1]
                descricao = l[2]
                data = l[3]
                prioridade = l[4]
                grupo = l[5]
                status = l[6]
                email = l[9]
                print(l)
                try:
                    if banco.usuarioExiste(email):
                        # Usuário existe, então cadastre a tarefa
                        recebeu = banco.cadastrar_tarefa(titulo, descricao, data, prioridade, grupo, status, email)
                        if recebeu == '1':
                            envia = '1'
                            print(f'Nova tarefa criada: {titulo}')
                        else:
                            envia = '0'
                    else:
                        # Usuário não existe, levanta uma exceção
                        raise ValueError('Usuário não encontrado. Cadastre o usuário antes de criar a tarefa.' + email)
                except Exception as e:
                    # Trate a exceção e forneça uma mensagem de erro adequada
                    envia = '0'
                    print(f"Erro ao cadastrar tarefa: {e}")

        except Exception as e:
            print(f"Erro ao criar tarefa: {e}")
            envia = '0'  # Handle the exception and set envia to '0' or another suitable value


    elif l[0] == '4':
        #verifica se o email existe
        if banco.emailExiste(l[1]):
            envia = '1'
        else:
            envia = '0'
    elif l[0] == '5':
        #envia a tabela de tarefas
        email = l[1]
        try:
            envia = banco.obter_tarefas(email)
        except Exception as e:
            print(f"Erro server  ao obter tarefas: {e}")
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
                # Garanta que enviar seja uma string antes de chamar encode()
                if isinstance(enviar, list):
                    enviar = str(enviar)
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
