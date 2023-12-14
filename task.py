#tabela de tarefas:
# CREATE TABLE Tarefas (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     descricao TEXT,
#     status VARCHAR(20) DEFAULT 'pendente',
#     usuario_email VARCHAR(255),
#     FOREIGN KEY (usuario_email) REFERENCES User(email)
# );

class Tarefa():
    def __init__(self, titulo, data, grupo):
        self.titulo = titulo
        self.data = data
        self.grupo = grupo

    def getTitulo(self):
        return self.titulo

    def getData(self):
        return self.data

    def getGrupo(self):
        return self.grupo

    def setTitulo(self, titulo):
        self.titulo = titulo

    def setData(self, data):
        self.data = data

    def setGrupo(self, grupo):
        self.grupo = grupo

    def __str__(self):
        return f"{self.titulo}, {self.data}, {self.grupo}"