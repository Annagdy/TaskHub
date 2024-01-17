import mysql.connector
from mysql.connector import Error
import pandas as pd

def create_server_connection(host_name, user_name, user_password):
    """
    Cria uma conexão com o servidor MySQL.

    Parameters
    ----------
    host_name : str
        Nome do host do servidor MySQL.
    user_name : str
        Nome do usuário do banco de dados.
    user_password : str
        Senha do usuário do banco de dados.

    Returns
    -------
    mysql.connector.connection or None
        Retorna o objeto de conexão se bem-sucedido, None em caso de erro.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_db_connection(host_name, user_name, user_password, db_name):
    """
    Cria uma conexão com um banco de dados específico no servidor MySQL.

    Parameters
    ----------
    host_name : str
        Nome do host do servidor MySQL.
    user_name : str
        Nome do usuário do banco de dados.
    user_password : str
        Senha do usuário do banco de dados.
    db_name : str
        Nome do banco de dados.

    Returns
    -------
    mysql.connector.connection or None
        Retorna o objeto de conexão se bem-sucedido, None em caso de erro.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query):
    """
    Executa uma query no banco de dados.

    Parameters
    ----------
    connection : mysql.connector.connection
        Objeto de conexão com o banco de dados.
    query : str
        String contendo a query SQL a ser executada.

    Returns
    -------
    None
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
