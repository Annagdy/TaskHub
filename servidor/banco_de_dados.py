import mysql.connector as mysql
import datetime
from PyQt5.QtCore import QCoreApplication

class Banco:
    def __init__(self) -> None:
        self.conexao = mysql.connect(host='localhost', database='poo2', user='root', password='z321')
        self.cursor = self.conexao.cursor()

        self.usuario_logado = None

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS User (
                        username VARCHAR(255) NOT NULL,
                        email VARCHAR(255) PRIMARY KEY NOT NULL,
                        senha VARCHAR(100) NOT NULL
                     )''')

        # self.cursor.execute('''CREATE TABLE IF NOT EXISTS User (
        #     user_name VARCHAR(100) NOT NULL,
        #     email VARCHAR(255) PRIMARY KEY NOT NULL,
        #     senha VARCHAR(100) NOT NULL,
        # )''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tarefas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            descricao VARCHAR(500) NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'Pendente',
            FOREIGN KEY (usuario_email) REFERENCES User(email)
        )''')
        
    def cadastrar_usuario(self, user_name, email, senha):
        try:
            self.cursor.execute(f"INSERT INTO User VALUES ('{user_name}', '{email}', '{senha}')")
            self.conexao.commit()
            return True
        except:
            return False
    
    def obter_email_usuario_logado(self):
        if self.usuario_logado is None:
            self.cursor.execute(f"SELECT email FROM User WHERE email = '{self.usuario_logado}'")
            resultado = self.cursor.fetchone()
            if resultado is not None:
                return resultado[0]
        return None
    
    def obter_nome_usuario_logado(self):
        if self.usuario_logado is None:
            self.cursor.execute(f"SELECT user_name FROM User WHERE email = '{self.usuario_logado}'")
            resultado = self.cursor.fetchone()
            if resultado is not None:
                return resultado[0]
        return None

    def logar_usuario(self, email, senha):
        self.cursor.execute(f"SELECT * FROM User WHERE email = '{email}' AND senha = '{senha}'")
        resultado = self.cursor.fetchone()
        if resultado is not None:
            self.obter_email_usuario_logado()
            return True
        return False
    
   
    
    
    

