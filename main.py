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

        self.cad = Cadastro()
        self.login_tela.confirmarLogin.clicked.connect(self.botaoLogin)
        self.login_tela.cadastrar.clicked.connect(self.abrirTelaCadastro)
        self.login_tela.fecharBota.clicked.connect(exit)

        self.cadastro_tela.confirmar.clicked.connect(self.botaoCadastra)
        self.cadastro_tela.voltarBotao.clicked.connect(self.returnIndex)

        self.tela_principal.pushButton.clicked.connect(self.returnIndex)

        self.tela_principal.Criar.clicked.connect(self.botaoCriar)
        
        self.tarefa.cancel.clicked.connect(self.telaPrinc)

        pessoal_tarefas = ["Fazer POO2", "Fazer ED2"]
        tarefas_tempo = ["terça, 14", "quinta, 19"]
        self.tela_principal.listaTodo.setColumnCount(3)

        self.tela_principal.listaTodo.horizontalHeader().setVisible(False)
        self.tela_principal.listaTodo.verticalHeader().setVisible(False)

        self.tela_principal.listaTodo.setColumnWidth(0, 10)

        for row, tarefa in enumerate(pessoal_tarefas):
            self.tela_principal.listaTodo.insertRow(row)

            item_widget = QTableWidgetItem(tarefa)
            self.tela_principal.listaTodo.setItem(row, 1, item_widget)

            checkbox = QCheckBox()
            checkbox.setChecked(False)
            self.tela_principal.listaTodo.setCellWidget(row, 0, checkbox)

            for row, tempo in enumerate(tarefas_tempo):
                item_widget = QTableWidgetItem(tempo)
                self.tela_principal.listaTodo.setItem(row, 2, item_widget)

        

    def botaoCadastra(self):
        usuario = self.cadastro_tela.usuario_linha.text()
        email = self.cadastro_tela.email_linha.text()
        senha = self.cadastro_tela.senha_linha.text()

        if not(usuario == '' or email == '' or senha == '' or usuario == ' ' or email == ' ' or senha == ' '):

            connection = create_db_connection("localhost", "root", "9437AP", "poo2")

            insert_query = f"INSERT INTO User (user_id, email, senha) VALUES ('{usuario}', '{email}', '{senha}')"

            execute_query(connection, insert_query)

            if self.cad.cadastra(usuario, email, senha):  # Modifique o método 'cadastra' para aceitar os campos corretos
                QMessageBox.information(None, 'TaskHub', 'Cadastro Realizado com Sucesso!')
                self.cadastro_tela.usuario_linha.setText('')
                self.cadastro_tela.email_linha.setText('')
                self.cadastro_tela.senha_linha.setText('')
            else:
                QMessageBox.information(None, 'TaskHub', 'Usuário Já Cadastrado')
        else:
            QMessageBox.information(None, 'TaskHub', 'Preencha Todos os Campos!')

        self.Qtstack.setCurrentIndex(0)

    def botaoLogin(self):
        email = self.login_tela.email_linha.text()
        senha = self.login_tela.senha_linha.text()


        if not(email == '' or senha == ''):
            connection = create_db_connection("localhost", "root", "9437AP", "poo2")

            select_query = f"SELECT * FROM User WHERE email = '{email}' AND senha = '{senha}'"
            cursor = connection.cursor()
            cursor.execute(select_query)
            result = cursor.fetchone()

            if result:
                usuario, _, _ = result  # Os dados estão na ordem da consulta
                QMessageBox.information(None, 'TaskHub', 'Login Realizado com Sucesso!')
                self.Qtstack.setCurrentIndex(2)
                self.tela_principal.linha_user.setText(usuario)
                        
                self.login_tela.email_linha.clear()
                self.login_tela.senha_linha.clear()
            else:
                self.Qtstack.setCurrentIndex(0)
                QMessageBox.information(None, 'TaskHub', 'Email ou Senha Incorretos!')
                
                self.login_tela.email_linha.clear()
                self.login_tela.senha_linha.clear()

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


    connection = create_server_connection("localhost", "root", "9437AP")
    
    connection = create_db_connection("localhost", "root", "9437AP", "poo2")

    sys.exit(app.exec_())