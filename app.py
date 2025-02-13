from flask import Flask, render_template, request, redirect, url_for
import pymysql
import os

app = Flask(__name__)

# Configuracao do banco de dados

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='1234',
        database='books_proj'
    )

#Rota para Livros
@app.route('/books')
def books():
    # Conectar ao banco de dados
    db = get_db_connection()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    # Buscar os livros
    cursor.execute("SELECT * FROM livros")
    livros = cursor.fetchall()

    # Fechar a conexão com o banco de dados
    cursor.close()
    db.close()

    # Passar os livros para o template 'books.html'
    return render_template('books.html', livros=livros)

# Para adicionar ou atualizar um livro
@app.route('/add_book', methods=['POST'])
def add_book():
    nome_livro = request.form.get('nome_livro')
    quant_livro = int(request.form.get('quant_livro'))

    # Verifica se os campos estão preenchidos corretamente
    if not nome_livro or quant_livro <= 0:
        print("Os campos nome_livro e quant_livro são obrigatórios e a quantidade deve ser maior que 0!")
        return redirect(url_for('books'))

    db = get_db_connection()
    try:
        cursor = db.cursor(pymysql.cursors.DictCursor)
        
        # Verifica se o livro já existe
        sql_check = "SELECT * FROM livros WHERE nome_livro = %s"
        cursor.execute(sql_check, (nome_livro,))
        livro_existente = cursor.fetchone()
        
        if livro_existente:
            # Atualiza a quantidade do livro existente
            nova_quantidade = livro_existente['quant_livro'] + quant_livro
            sql_update = "UPDATE livros SET quant_livro = %s WHERE id = %s"
            cursor.execute(sql_update, (nova_quantidade, livro_existente['id']))
            print(f"Quantidade do livro '{nome_livro}' atualizada para {nova_quantidade}.")
        else:
            # Insere um novo livro
            sql_insert = "INSERT INTO livros (nome_livro, quant_livro) VALUES (%s, %s)"
            cursor.execute(sql_insert, (nome_livro, quant_livro))
            print(f"Livro '{nome_livro}' adicionado com sucesso!")
        
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Erro ao adicionar ou atualizar livro: {e}")
    finally:
        cursor.close()
        db.close()
    
    return redirect(url_for('books'))

# Deletar um livro
@app.route('/delete_book/<int:id>')
def delete_book(id):
    db = get_db_connection()
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM livros WHERE id = %s", (id,))
        db.commit()
        print("Livro deletado com sucesso!")
    except Exception as e:
        db.rollback()
        print(f"Erro ao deletar livro: {e}")
    finally:
        cursor.close()
        db.close()
    
    return redirect(url_for('books'))

# Para listar usuarios
@app.route('/')
def index():
    cursor = get_db_connection().cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    return render_template('index.html', usuarios=usuarios)

# Para adicionar um usuario
@app.route('/add', methods=['POST'])
def add_user():
    # Captura os dados do formulário
    nome = request.form.get('nome')
    ra = request.form.get('ra')
    
    # Se estiver tudo certo, conecta ao banco de dados e insere o usuário
    db = get_db_connection()
    try:
        cursor = db.cursor()
        sql = "INSERT INTO usuarios (nome, ra) VALUES (%s, %s)"
        cursor.execute(sql, (nome, ra))
        db.commit()
        print("Usuário adicionado com sucesso!")
    except Exception as e:
        db.rollback()  # Reverte a transação em caso de erro
        print(f"Erro ao adicionar usuário: {e}")
    finally:
        cursor.close()
        db.close()
    
    return redirect(url_for('index'))

# Deletar um usuario
@app.route('/delete/<int:id>')
def delete_user(id):
    db = get_db_connection()  
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        db.commit()  
        print("Usuário deletado com sucesso!")
    except Exception as e:
        db.rollback()  
        print(f"Erro ao deletar usuário: {e}")
    finally:
        cursor.close()  
        db.close()  

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
