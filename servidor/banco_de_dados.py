import mysql.connector as mysql
import datetime
from PyQt5.QtCore import QCoreApplication

class Banco:
    def __init__(self) -> None:
        """
        Construtor da classe Banco.

        Este construtor inicializa a conexão com o banco de dados MySQL, cria as tabelas necessárias,
        e inicializa algumas variáveis de controle.

        Attributes
        ----------
        conexao : mysql.connector.connection
            Objeto de conexão com o banco de dados.
        cursor : mysql.connector.cursor
            Cursor para executar comandos SQL.
        usuario_logado : str
            Email do usuário logado, inicializado como None.

        Tables
        ------
        User : Tabela para armazenar informações do usuário.
            Campos: user_name, email, senha.

        tarefas : Tabela para armazenar informações das tarefas.
            Campos: id, descricao, status, usuario_email (referência à tabela User).

        """
        self.conexao = mysql.connect(host='localhost', database='poo2', user='root', password='z321')
        self.cursor = self.conexao.cursor()

        self.usuario_logado = None

        # Criação das tabelas se não existirem
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS User (
                        user_name VARCHAR(255) NOT NULL,
                        email VARCHAR(255) PRIMARY KEY NOT NULL,
                        senha VARCHAR(100) NOT NULL
                     )''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tarefas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            descricao VARCHAR(500) NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'Pendente',
            FOREIGN KEY (usuario_email) REFERENCES User(email)
        )''')
        
    def cadastrar_usuario(self, user_name, email, senha):
        """
        Cadastra um novo usuário no banco de dados.

        Parameters
        ----------
        user_name : str
            Nome do usuário.
        email : str
            Email do usuário (chave primária).
        senha : str
            Senha do usuário.

        Returns
        -------
        bool
            Retorna True se o cadastro for bem-sucedido, False caso contrário.
        """
        try:
            self.cursor.execute(f"INSERT INTO User VALUES ('{user_name}', '{email}', '{senha}')")
            self.conexao.commit()
            return True
        except:
            return False
    
    def obter_email_usuario_logado(self):
        """
        Obtém o email do usuário logado.

        Returns
        -------
        str or None
            Retorna o email do usuário logado ou None se nenhum usuário estiver logado.
        """
        if self.usuario_logado is not None:
            return self.usuario_logado
        return None
    
    def obter_nome_usuario_logado(self):
        """
        Obtém o nome do usuário logado.

        Returns
        -------
        str or None
            Retorna o nome do usuário logado ou None se nenhum usuário estiver logado.
        """
        if self.usuario_logado is not None:
            self.cursor.execute(f"SELECT user_name FROM User WHERE email = '{self.usuario_logado}'")
            resultado = self.cursor.fetchone()
            if resultado is not None:
                return resultado[0]
        return None

    def logar_usuario(self, email, senha):
        """
        Realiza o login de um usuário.

        Parameters
        ----------
        email : str
            Email do usuário.
        senha : str
            Senha do usuário.

        Returns
        -------
        bool
            Retorna True se o login for bem-sucedido, False caso contrário.
        """
        self.cursor.execute(f"SELECT * FROM User WHERE email = '{email}' AND senha = '{senha}'")
        resultado = self.cursor.fetchone()
        if resultado is not None:
            self.usuario_logado = email
            return True
        return False
    
    def usuarioExiste(self, usuario_email):
        """
        Verifica se um usuário existe.

        Parameters
        ----------
        usuario_email : str
            Email do usuário.

        Returns
        -------
        bool
            Retorna True se o usuário existir, False caso contrário.
        """
        self.cursor.execute(f"SELECT * FROM User WHERE email = '{usuario_email}'")
        resultado = self.cursor.fetchone()
        if resultado is not None:
            return True
        return False
