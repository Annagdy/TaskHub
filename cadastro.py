from PyQt5.QtWidgets import *
from pessoa import Pessoa

class Cadastro():
    """
    Classe que representa um sistema de cadastro de usuários.

    Attributes
    ----------
    _lista_pessoas : list
        Lista de objetos Pessoa cadastrados.

    Methods
    -------
    __init__(self)
        Construtor da classe. Inicializa a lista de pessoas.
        
    cadastra(self, usuario, email, senha)
        Cadastra uma nova Pessoa se o email não estiver duplicado.
        
    busca(self, email)
        Busca uma Pessoa na lista pelo email.
    """

    __slots__ = ('_lista_pessoas')

    def __init__(self):
        """
        Construtor da classe. Inicializa a lista de pessoas.
        """
        self._lista_pessoas = []
    
    def cadastra(self, usuario, email, senha):
        """
        Cadastra uma nova Pessoa se o email não estiver duplicado.

        Parameters
        ----------
        usuario : str
            Nome do usuário.
        email : str
            Email do usuário (deve ser único).
        senha : str
            Senha do usuário.

        Returns
        -------
        bool
            Retorna True se o cadastro for bem-sucedido, False se o email já estiver cadastrado.
        """
        p = Pessoa(usuario, email, senha)
        existe = self.busca(p.email)

        if existe is None:
            self._lista_pessoas.append(p)
            return True
        else:
            return False
    
    def busca(self, email):
        """
        Busca uma Pessoa na lista pelo email.

        Parameters
        ----------
        email : str
            Email da Pessoa a ser buscada.

        Returns
        -------
        Pessoa or None
            Retorna a Pessoa se encontrada, None se não encontrada.
        """
        for pessoa in self._lista_pessoas:
            if pessoa.email == email:
                return pessoa
        return None
