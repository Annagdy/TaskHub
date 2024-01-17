class Pessoa():
    """
    Classe que representa uma pessoa com informações de usuário.

    Attributes
    ----------
    _usuario : str
        Nome do usuário.
    _email : str
        Email do usuário.
    _senha : str
        Senha do usuário.

    Methods
    -------
    __init__(self, usuario, email, senha)
        Construtor da classe. Inicializa os atributos da pessoa.
    """

    def __init__(self, usuario, email, senha):
        """
        Construtor da classe. Inicializa os atributos da pessoa.

        Parameters
        ----------
        usuario : str
            Nome do usuário.
        email : str
            Email do usuário.
        senha : str
            Senha do usuário.
        """
        self._usuario = usuario
        self._email = email
        self._senha = senha
    
    @property
    def usuario(self):
        """
        Getter para obter o nome do usuário.

        Returns
        -------
        str
            Nome do usuário.
        """
        return self._usuario

    @property
    def email(self):
        """
        Getter para obter o email do usuário.

        Returns
        -------
        str
            Email do usuário.
        """
        return self._email
    
    @property
    def senha(self):
        """
        Getter para obter a senha do usuário.

        Returns
        -------
        str
            Senha do usuário.
        """
        return self._senha
    
    @email.setter
    def email_set(self, email):
        """
        Setter para atualizar o email do usuário.

        Parameters
        ----------
        email : str
            Novo email do usuário.

        Returns
        -------
        None
        """
        self._email = email
    
    @senha.setter
    def senha_set(self, senha):
        """
        Setter para atualizar a senha do usuário.

        Parameters
        ----------
        senha : str
            Nova senha do usuário.

        Returns
        -------
        None
        """
        self._senha = senha

    @usuario.setter
    def user_set(self, usuario):
        """
        Setter para atualizar o nome do usuário.

        Parameters
        ----------
        usuario : str
            Novo nome do usuário.

        Returns
        -------
        None
        """
        self._usuario = usuario
