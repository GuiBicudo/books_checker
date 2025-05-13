import pymysql

def get_db_connection():
    return pymysql.connect(
        host='localhost',         # ou outro host, se necessário
        user='root',       # substitua pelo nome do usuário do seu banco
        password='1234',     # substitua pela senha correta
        database='bookhub',       # substitua pelo nome do seu banco
        cursorclass=pymysql.cursors.DictCursor  # para retornar resultados como dicionários
    )
