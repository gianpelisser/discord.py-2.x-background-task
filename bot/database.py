import sqlalchemy
import mysql.connector
import settings


# MySQL: Verificar Players Online
def check_sql_players_on():
    myconexao = mysql.connector.connect(
        host=settings.mysql_host,
        port=settings.mysql_port,
        user=settings.mysql_user,
        password=settings.mysql_pass,
        database=settings.mysql_mydb)

    # Criar uma sessão para o mysql
    mycursor = myconexao.cursor()

    # consulta SQL
    mycursor.execute("SELECT isAvailable, usersOnline FROM teraapi.server_info WHERE serverId = 2800")
    # mycursor.execute("SELECT * FROM teraapi.server_info WHERE serverId = 2800")

    # Obter nomes das colunas
    columns = [column[0] for column in mycursor.description]

    # Resultado(s) da consulta
    row_resultados = mycursor.fetchone()

    # Combina os nomes das colunas com os valores
    resultado_dict = dict(zip(columns, row_resultados))

    myconexao.close()
    return resultado_dict
