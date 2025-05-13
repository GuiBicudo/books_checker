from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection # funcao de conexao com o db

app = Flask(__name__)
app.secret_key = 'segredo_super_secreto'  

# Configuração do banco de dados
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='1234',
        database='books_proj'
    )

# Rota para listar alunos (apenas para professores)
@app.route('/')
def index():
    if 'user_id' not in session or session['user_tipo'] != 'Professor':
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM alunos WHERE tipo = 'Aluno'")
    alunos = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('index.html', alunos=alunos)

# Código de criação de conta de professor
CODIGO_DE_PROFESSOR = 'Conexia123'

# Rota para registrar um novo aluno ou professor
@app.route('/register', methods=['GET', 'POST'])
def register():
    error_message = None  # Variável para armazenar a mensagem de erro

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        tipo = request.form['tipo']
        senha_criacao = request.form['senha_criacao']
        
        if not senha_criacao:
            return "A senha de criação de conta é obrigatória!", 400

        # Conexão com o banco de dados
        db = get_db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        try:
            # Verifica se o email já está registrado
            cursor.execute("SELECT * FROM alunos WHERE email = %s", (email,))
            existing_user = cursor.fetchone()

            # Verifica se o RA já está registrado (se for aluno)
            existing_ra = None
            ra = request.form.get('ra')

            if tipo == 'Aluno' and ra:
                cursor.execute("SELECT * FROM alunos WHERE ra = %s", (ra,))
                existing_ra = cursor.fetchone()
            
            # Validações
            if existing_user:
                error_message = "Este e-mail já está registrado! Escolha outro."
            elif existing_ra:
                error_message = "Este RA já está registrado! Escolha outro."
            elif tipo == 'Aluno' and not ra:
                error_message = "O RA é obrigatório para alunos!"
            elif tipo == 'Professor':
                codigo_professor = request.form.get('codigo_professor')
                if not codigo_professor or codigo_professor != CODIGO_DE_PROFESSOR:
                    error_message = "Código de criação de conta de professor incorreto!"

            # Se não houver erro, cria o usuário no banco
            if not error_message:
                senha_hash = generate_password_hash(senha_criacao)

                if tipo == 'Professor':
                    sql = "INSERT INTO alunos (nome, email, senha, tipo) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (nome, email, senha_hash, tipo))
                elif tipo == 'Aluno':
                    sql = "INSERT INTO alunos (nome, email, senha, tipo, ra) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql, (nome, email, senha_hash, tipo, ra))

                db.commit()
                return redirect(url_for('login'))

        except Exception as e:
            db.rollback()
            print(f"Erro ao registrar: {e}")
        finally:
            cursor.close()
            db.close()

    return render_template('register.html', error_message=error_message)

# Rota para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        db = get_db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM alunos WHERE email = %s", (email,))
        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user and check_password_hash(user['senha'], senha):
            session['user_id'] = user['id']
            session['user_nome'] = user['nome']  # Armazenando o nome do usuário
            session['user_tipo'] = user['tipo']

            # Redireciona para a página correta com base no tipo de usuário
            if user['tipo'] == 'Professor':
                return redirect(url_for('books'))  # Redireciona para a página de livros
            else:
                return redirect(url_for('aluno_dashboard'))  # Redireciona para a nova página do aluno

        return "E-mail ou senha incorretos!", 401  # Exibe erro se login falhar

    return render_template('login.html')

# Rota para a página principal pós-login
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session['user_tipo'] == 'Professor':
        return redirect(url_for('books'))  # Redireciona para a página de livros
    else:
        return redirect(url_for('aluno_dashboard'))  # Página do aluno 
    
# Rota para o Dashboard do Aluno, caso o usuario seja aluno.
@app.route('/aluno_dashboard')
def aluno_dashboard():
    if 'user_id' not in session or session['user_tipo'] != 'Aluno':
        return redirect(url_for('login'))  # Se não for aluno, redireciona para o login

    # Conectar ao banco de dados e buscar os livros disponíveis
    db = get_db_connection()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM livros")
    livros = cursor.fetchall()  # Obtém todos os livros
    cursor.close()
    db.close()

    return render_template('student-dashboard.html', livros=livros)  # Passa os livros para o template

# Rota para adicionar um aluno (apenas para professores)
@app.route('/add_aluno', methods=['POST'])
def add_aluno():
    if 'user_id' not in session or session['user_tipo'] != 'Professor':
        return redirect(url_for('login'))

    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = generate_password_hash(request.form.get('senha'))  # Hash da senha
    ra = request.form.get('ra')  # Capturando o RA

    # Caso o RA não seja fornecido, pode ser atribuído como None ou uma string vazia
    if ra == "":
        ra = None

    db = get_db_connection()
    try:
        cursor = db.cursor()
        # Caso o RA esteja presente, ele será incluído no banco de dados
        if ra:
            sql = "INSERT INTO alunos (nome, email, senha, tipo, ra) VALUES (%s, %s, %s, 'Aluno', %s)"
            cursor.execute(sql, (nome, email, senha, ra))
        else:
            sql = "INSERT INTO alunos (nome, email, senha, tipo) VALUES (%s, %s, %s, 'Aluno')"
            cursor.execute(sql, (nome, email, senha))

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Erro ao adicionar aluno: {e}")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('index'))

# Rota para deletar um aluno (apenas para professores)
@app.route('/delete_aluno/<int:id>')
def delete_aluno(id):
    if 'user_id' not in session or session['user_tipo'] != 'Professor':
        return redirect(url_for('login'))

    db = get_db_connection()
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM alunos WHERE id = %s", (id,))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Erro ao deletar aluno: {e}")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('index'))

#Rota para adicionar um livro
@app.route('/add_book', methods=['POST'])
def add_book():
    if 'user_id' not in session or session['user_tipo'] != 'Professor':
        return redirect(url_for('login'))

    nome_livro = request.form.get('nome_livro')
    quant_livro = int(request.form.get('quant_livro'))

    db = get_db_connection()
    try:
        cursor = db.cursor(pymysql.cursors.DictCursor)  # Assegurando que o cursor retorna um dicionário

        # Verificar se o livro já existe no banco de dados
        cursor.execute("SELECT * FROM livros WHERE nome_livro = %s", (nome_livro,))
        livro_existente = cursor.fetchone()

        if livro_existente:
            # Se o livro já existe, atualize a quantidade
            nova_quantidade = livro_existente['quant_livro'] + quant_livro
            cursor.execute("UPDATE livros SET quant_livro = %s WHERE nome_livro = %s", (nova_quantidade, nome_livro))
            print(f'Quantidade do livro "{nome_livro}" atualizada para {nova_quantidade}')
        else:
            # Se o livro não existir, insira um novo livro
            cursor.execute("INSERT INTO livros (nome_livro, quant_livro) VALUES (%s, %s)", (nome_livro, quant_livro))
            print(f'Novo livro "{nome_livro}" adicionado com quantidade {quant_livro}')

        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Erro ao adicionar/atualizar livro: {e}")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('books'))

# Rota para deletar um livro (apenas para professores)
@app.route('/delete_book/<int:id>')
def delete_book(id):
    if 'user_id' not in session or session['user_tipo'] != 'Professor':
        return redirect(url_for('login'))

    db = get_db_connection()
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM livros WHERE id = %s", (id,))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Erro ao deletar livro: {e}")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('books'))

# Rota para logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Rota para listar livros (apenas para usuários logados)
@app.route('/books')
def books():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redireciona se não estiver logado

    db = get_db_connection()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM livros")
    livros = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('books.html', livros=livros)

# Rota principal do fórum
@app.route('/forum', methods=['GET', 'POST'])
def view_forum():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = session.get('user_id')

        if user_id:
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute('INSERT INTO forum_posts (user_id, title, content) VALUES (%s, %s, %s)', (user_id, title, content))
            db.commit()
            cursor.close()
            db.close()
            # Após a postagem, você pode querer recarregar os posts
            return redirect(url_for('view_forum')) # Redireciona para a mesma página para exibir a nova postagem
        else:
            return redirect(url_for('login')) # Se o usuário não estiver logado

    db = get_db_connection()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT f.id, f.title, f.content, f.created_at, u.nome AS username FROM forum_posts f JOIN alunos u ON f.user_id = u.id ORDER BY f.created_at DESC')
    posts = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('forum.html', posts=posts)

# Rota para visualizar uma postagem individual com comentários
@app.route('/forum/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    db = get_db_connection()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    # Buscar a postagem
    cursor.execute('SELECT f.id, f.title, f.content, f.created_at, u.nome AS username FROM forum_posts f JOIN alunos u ON f.user_id = u.id WHERE f.id = %s', (post_id,))
    post = cursor.fetchone()

    if not post:
        return "Postagem não encontrada!", 404

    # Buscar os comentários da postagem
    cursor.execute('SELECT c.id, c.text, c.created_at, u.nome AS username FROM forum_comments c JOIN alunos u ON c.user_id = u.id WHERE c.post_id = %s ORDER BY c.created_at ASC', (post_id,))
    comments = cursor.fetchall()

    if request.method == 'POST':
        if 'user_id' not in session:
            return redirect(url_for('login'))  # Redireciona se não estiver logado

        comment_text = request.form['comment_text']
        user_id = session['user_id']

        cursor.execute('INSERT INTO forum_comments (post_id, user_id, text) VALUES (%s, %s, %s)', (post_id, user_id, comment_text))
        db.commit()
        # Recarrega a página para exibir o novo comentário
        return redirect(url_for('view_post', post_id=post_id))

    cursor.close()
    db.close()
    return render_template('post.html', post=post, comments=comments)

if __name__ == '__main__':
    app.run(debug=True)

# Conteúdo do seu forum.py (você pode simplificar ou remover se toda a lógica estiver no app.py)
from flask import Blueprint, render_template

forum = Blueprint('forum', __name__, template_folder='templates')