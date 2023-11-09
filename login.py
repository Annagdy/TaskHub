from PyQt5.QtWidgets import *
from login_tela import Login_Tela
from cadastro import Cadastro
from pessoa import Pessoa

class Login():
    def __init__(self):
        super().__init__()

        self.cad = Cadastro()
        self.login_tela = Login_Tela()

        self.p = Pessoa()

    def fazer_login(self, email, senha):
        pessoa = self.cad.busca(email)

        if pessoa and pessoa.senha == senha:
            QMessageBox.information(None, 'TaskHub', 'Login Sucedido!')

            return pessoa
        else:
            QMessageBox.information(None, 'TaskHub', 'Email ou Senha Incorretos!')

            return None