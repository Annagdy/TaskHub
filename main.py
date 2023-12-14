import sys
import typing

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QWidget, QTableWidget, QTableWidgetItem, QCheckBox

from login_tela import Login_Tela
from cadastro_tela import Cadastro_Tela
from tela_principal import Tela_Principal
from tarefa import Tela_Tarefa
from pessoa import Pessoa
from cadastro import Cadastro
from login import Login
from task import Tarefa
from cliente import Cliente

import mysql.connector
from mysql.connector import Error
import pandas as pd


from database import create_db_connection, create_server_connection, execute_query

class Ui_Main(QtWidgets.QWidget):
    def setupUi(self, Main):
        Main.setObjectName("TaskHub")
        Main.setWindowTitle("TaskHub")
        
        self.Qtstack = QtWidgets.QStackedLayout()

        self.stack0 = QtWidgets.QMainWindow()
        self.stack1 = QtWidgets.QMainWindow()
        self.stack2 = QtWidgets.QMainWindow()
        self.stack3 = QtWidgets.QMainWindow()

        self.login_tela = Login_Tela()
        self.login_tela.setupUi(self.stack0)
        self.login_tela.senha_linha.setEchoMode(self.login_tela.senha_linha.Password)

        self.cadastro_tela = Cadastro_Tela()
        self.cadastro_tela.setupUi(self.stack1)
        self.cadastro_tela.senha_linha.setEchoMode(self.cadastro_tela.senha_linha.Password)

        self.tela_principal = Tela_Principal()
        self.tela_principal.setupUi(self.stack2)

        self.tarefa = Tela_Tarefa()
        self.tarefa.setupUi(self.stack3)

        self.Qtstack.addWidget(self.stack0)
        self.Qtstack.addWidget(self.stack1)
        self.Qtstack.addWidget(self.stack2)
        self.Qtstack.addWidget(self.stack3)

class Main(QMainWindow, Ui_Main):
    def __init__(self):
        super(Main, self).__init__(None)
        self.setupUi(self)

        self.usuario_logado = None
        self.username = None
        self.cliente = Cliente()
        self.cad = Cadastro()

        self.login_tela.confirmarLogin.clicked.connect(self.botaoLogin)
        self.login_tela.cadastrar.clicked.connect(self.abrirTelaCadastro)
        self.login_tela.fecharBota.clicked.connect(exit)

        self.cadastro_tela.confirmar.clicked.connect(self.botaoCadastra)
        self.cadastro_tela.voltarBotao.clicked.connect(self.returnIndex)

        self.tela_principal.pushButton.clicked.connect(self.returnIndex)

        self.tela_principal.Criar.clicked.connect(self.botaoCriar)
        
        self.tarefa.cancel.clicked.connect(self.telaPrinc)

        self.tarefa.conf.clicked.connect(self.botaoCriaTarefa)

        # self.tarefa.conf.clicked.connect(self.botaoConfirmaTarefa)


        # pessoal_tarefas = ["Fazer POO2", "Fazer ED2"]
        # tarefas_tempo = ["terça, 14", "quinta, 19"]
        self.tela_principal.listaTodo.setColumnCount(3)

        self.tela_principal.listaTodo.horizontalHeader().setVisible(False)
        self.tela_principal.listaTodo.verticalHeader().setVisible(False)

        self.tela_principal.listaTodo.setColumnWidth(0, 10)

    
        # Estabeleça uma conexão com o banco de dados
        connection = create_db_connection("localhost", "root", "z321", "poo2")

        # Execute uma consulta SQL para obter todas as tarefas
        select_query = "SELECT * FROM Tarefas"
        tarefas = execute_query(connection, select_query)

        # Limpe a tabela antes de adicionar novos itens
        self.tela_principal.listaTodo.setRowCount(0)


        if tarefas is not None:
            for row, tarefa in enumerate(tarefas):
                self.tela_principal.listaTodo.insertRow(row)

                item_widget = QTableWidgetItem(tarefa)
                self.tela_principal.listaTodo.setItem(row, 1, item_widget)

                checkbox = QCheckBox()
                checkbox.setChecked(False)
                self.tela_principal.listaTodo.setCellWidget(row, 0, checkbox)

                
                item_widget = QTableWidgetItem(tarefa[3])
                self.tela_principal.listaTodo.setItem(row, 2, item_widget)
        else:
            print("Nenhuma tarefa encontrada")
        
        # for row, tarefa in enumerate(pessoal_tarefas):
            #     self.tela_principal.listaTodo.insertRow(row)

            #     item_widget = QTableWidgetItem(tarefa)
            #     self.tela_principal.listaTodo.setItem(row, 1, item_widget)

            #     checkbox = QCheckBox()
            #     checkbox.setChecked(False)
            #     self.tela_principal.listaTodo.setCellWidget(row, 0, checkbox)

            #     for row, tempo in enumerate(tarefas_tempo):
            #         item_widget = QTableWidgetItem(tempo)
            #         self.tela_principal.listaTodo.setItem(row, 2, item_widget)

    def usuarioExiste(self, usuario_email):
        connection = create_db_connection("localhost", "root", "z321", "poo2")
        cursor = connection.cursor()

        select_user_query = f"SELECT * FROM User WHERE email = '{usuario_email}'"
        cursor.execute(select_user_query)
        result = cursor.fetchone()

        # Verifique se o usuário existe
        return result is not None
    
    

    def botaoCriaTarefa(self):
        titulo = self.tarefa.title_taf.text()
        data = self.tarefa.date.text()
        grupo = self.tarefa.group_name.text()

        # Certifique-se de que o usuário está autenticado (substitua 'email' pelo email real do usuário autenticado)
        usuario_email  = self.tela_principal.linha_user.text()

        # Verifique se o usuário existe antes de criar a tarefa
        if self.usuarioExiste(usuario_email):
            try:
                # Inicie a transação
                connection = create_db_connection("localhost", "root", "z321", "poo2")
                cursor = connection.cursor()

                # Inserir tarefa
                insert_task_query = f"INSERT INTO Tarefas (descricao, status, usuario_email) VALUES ('{titulo}', 'pendente', '{usuario_email}')"
                cursor.execute(insert_task_query)

                # Commit da transação se tudo ocorrer sem problemas
                connection.commit()

                QMessageBox.information(None, 'TaskHub', 'Tarefa Criada com Sucesso!')
                self.tarefa.title_taf.setText('')
                self.tarefa.date.setText('')
                self.tarefa.group_name.setText()

                # Atualize a tabela na tela principal (se necessário)
                self.atualizarTabela()

            except Exception as e:
                # Em caso de erro, reverta a transação
                print(f"Error: {e}")
                connection.rollback()

            finally:
                # Feche a conexão
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        else:
            QMessageBox.information(None, 'TaskHub', 'Usuário não encontrado. Faça o login novamente.')

        self.Qtstack.setCurrentIndex(2)


    # def botaoCriaTarefa(self):
    #     titulo = self.tarefa.title_taf.text()
    #     data = self.tarefa.date.text()
    #     grupo = self.tarefa.group_name.text()

    #     #quero que a tarefa seja cadastrada na tabela de tarefas do banco de dados(conecte a tabela tarefas)
    #     #e que seja mostrada na tela principal
    #     # CREATE TABLE Tarefas (
    #     #     id INT PRIMARY KEY AUTO_INCREMENT,
    #     #     descricao TEXT,
    #     #     status VARCHAR(20) DEFAULT 'pendente',
    #     #     usuario_email VARCHAR(255),
    #     #     FOREIGN KEY (usuario_email) REFERENCES User(email)
    #     # );
    #     if not(titulo == '' or data == '' or grupo == '' or titulo == ' ' or data == ' ' or grupo == ' '):    
    #         #conexao com o banco de dados para salvar a tarefa
    #         connection = create_db_connection("localhost", "root", "z321", "poo2")

    #         insert_query = f"INSERT INTO Tarefas (descricao, status, usuario_email) VALUES ('{titulo}', 'pendente', 'email')"

    #         execute_query(connection, insert_query)

    #         if self.cad.cadastra(titulo, data, grupo):
    #             QMessageBox.information(None, 'TaskHub', 'Tarefa Criada com Sucesso!')
    #             self.tarefa.title_taf.setText('')
    #             self.tarefa.date.setText('')
    #             self.tarefa.group_name.setText('')
    #         else:
    #             QMessageBox.information(None, 'TaskHub', 'Tarefa Não Criada')
    #     else:
    #         QMessageBox.information(None, 'TaskHub', 'Preencha Todos os Campos!')

    #     self.Qtstack.setCurrentIndex(2)

    
    def botaoCadastra(self):
        usuario = self.cadastro_tela.usuario_linha.text()
        email = self.cadastro_tela.email_linha.text()
        senha = self.cadastro_tela.senha_linha.text()

        if not(usuario == '' or email == '' or senha == '' or usuario == ' ' or email == ' ' or senha == ' '):

            msg = '1' + '-' + usuario + '-' + email + '-' + senha

            recebeu = self.cliente.enviar(msg)
            if recebeu == '1':
                QMessageBox.information(None, 'TaskHub', 'Cadastro Realizado com Sucesso!')
                self.cadastro_tela.usuario_linha.setText('')
                self.cadastro_tela.email_linha.setText('')
                self.cadastro_tela.senha_linha.setText('')
                self.Qtstack.setCurrentIndex(0)
            else:
                QMessageBox.information(None, 'TaskHub', 'Email já cadastrado!')
                self.cadastro_tela.usuario_linha.setText('')
                self.cadastro_tela.email_linha.setText('')
                self.cadastro_tela.senha_linha.setText('')
        else:
            QMessageBox.information(None, 'TaskHub', 'Preencha Todos os Campos!')
            self.cadastro_tela.usuario_linha.setText('')
            self.cadastro_tela.email_linha.setText('')
            self.cadastro_tela.senha_linha.setText('')

    def botaoLogin(self):
        email = self.login_tela.email_linha.text()
        senha = self.login_tela.senha_linha.text()

        mensagem = '0' + '-' + email + '-' + senha
        resposta = self.cliente.enviar(mensagem)

        if resposta != '0':
            #pegar nome do usuario
            username = self.cliente.enviar('2' + '-' + email + '-' + senha)
            QMessageBox.information(None, 'TaskHub', 'Login Realizado com Sucesso!')
            self.Qtstack.setCurrentIndex(2)
            self.tela_principal.linha_user.setText(username)
            self.login_tela.email_linha.setText('')
            self.login_tela.senha_linha.setText('')
        else:
            QMessageBox.information(None, 'TaskHub', 'Email ou Senha Incorretos!')
            self.login_tela.email_linha.setText('')
            self.login_tela.senha_linha.setText('')


        # if not(email == '' or senha == ''):
        #     connection = create_db_connection("localhost", "root", "z321", "poo2")

        #     select_query = f"SELECT * FROM User WHERE email = '{email}' AND senha = '{senha}'"
        #     cursor = connection.cursor()
        #     cursor.execute(select_query)
        #     result = cursor.fetchone()

        #     if result:
        #         usuario, _, _ = result  # Os dados estão na ordem da consulta
        #         QMessageBox.information(None, 'TaskHub', 'Login Realizado com Sucesso!')
        #         self.Qtstack.setCurrentIndex(2)
        #         self.tela_principal.linha_user.setText(usuario)
                        
        #         self.login_tela.email_linha.clear()
        #         self.login_tela.senha_linha.clear()
        #     else:
        #         self.Qtstack.setCurrentIndex(0)
        #         QMessageBox.information(None, 'TaskHub', 'Email ou Senha Incorretos!')
                
        #         self.login_tela.email_linha.clear()
        #         self.login_tela.senha_linha.clear()



    def botaoCriar(self):
        self.Qtstack.setCurrentIndex(3)
    
    def telaPrinc(self):
        self.Qtstack.setCurrentIndex(2)

    def returnIndex(self):
        self.Qtstack.setCurrentIndex(0)

    def abrirTelaCadastro(self):
        self.Qtstack.setCurrentIndex(1)

    def abrirTelaPrincipal(self):
        self.Qtstack.setCurrentIndex(2)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    show_main = Main()

    sys.exit(app.exec_())
   
    