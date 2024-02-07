import socket 

class Cliente:
    """
    Classe que representa um cliente que se conecta a um servidor usando sockets.
    
    ...

    Attributes
    ----------
    ip : str
        O endereço IP do servidor.
    port : int
        A porta de conexão do servidor.
    address : tuple
        A tupla contendo o endereço IP e a porta de conexão.
    cliente_socket : socket
        O objeto de socket usado para a conexão com o servidor.


    Methods
    -------
    __init__(self)
        Construtor da classe. Inicializa a classe do cliente.
        
    enviar(self, mensagem)
        Envia uma mensagem para o servidor e recebe a resposta.
    """

    def __init__(self):
        """
        Parameters
        ----------
        ip : str
            O endereço IP do servidor.
        port : int
            A porta de conexão do servidor.
        address : tuple
            A tupla contendo o endereço IP e a porta de conexão.
        cliente_socket : socket
            O objeto de socket usado para a conexão com o servidor.
        """

        # Configuração inicial do cliente
        self.ip = '192.168.1.14'
        self.port = 8087
        self.address = (self.ip, self.port)
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente_socket.connect(self.address)

    def enviar(self, mensagem):
        """
        Envia uma mensagem para o servidor e recebe a resposta.

        A função enviar é responsável por enviar uma mensagem para o servidor e receber a resposta 
        correspondente. Essa função é responsável por estabelecer a comunicação entre o cliente e o
        servidor, enviando mensagens e recebendo as respostas correspondentes.

        Parameters
        ----------
        mensagem : str
            A mensagem a ser enviada para o servidor.

        Returns
        -------
        recebeu : str
            A resposta recebida do servidor.
        """

        # Envia a mensagem codificada para o servidor
        self.cliente_socket.send(mensagem.encode())
        
        # Recebe a resposta do servidor e decodifica
        recebeu = self.cliente_socket.recv(1024).decode()
        
        # Verifica se há uma instrução especial de encerramento
        verificador = recebeu.split(",")
        print(verificador)
        if verificador[0] == '-1':
            self.cliente_socket.close()
        
        # Retorna a resposta recebida do servidor
        return recebeu
