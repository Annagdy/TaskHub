class Pessoa():
    def __init__(self, usuario, email, senha):
        self._usuario = usuario
        self._email = email
        self._senha = senha
    
    @property
    def usuario(self):
        return self._usuario

    @property
    def email(self):
        return self._email
    
    @property
    def senha(self):
        return self._senha
    
    @email.setter
    def email_set(self, email):
        self._email = email
    
    @senha.setter
    def senha_set(self, senha):
        self._senha = senha

    @usuario.setter
    def user_set(self, usuario):
        self._usuario = usuario