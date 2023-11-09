from PyQt5.QtWidgets import *
from pessoa import Pessoa

class Cadastro():
    __slots__ = ('_lista_pessoas')

    def __init__(self):
        self._lista_pessoas = []
    
    def cadastra(self, usuario, email, senha):
        p = Pessoa(usuario, email, senha)
        existe = self.busca(p.email)

        if(existe == None):
            self._lista_pessoas.append(p)
            return True
        else:
            return False
    
    def busca(self, email):
        for ip in self._lista_pessoas:
            if ip.email == email:
                return ip
        return None
