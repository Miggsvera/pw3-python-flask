# Comentário no python
# Importando o flask para a aplicação
# do pacote do flask, importe a classe Flask
from controllers import routes
from flask import Flask, render_template

# Importando PYMYSQL
import pymysql
# Importando o SQLAlchemy e o Model
from models.database import db, Game

# Defindo um nome para o banco
DB_NAME = 'the_games'


# Importanto o Controller

# carregando o Flask na variável "app"
# declarando variável no python: nome = "..."
app = Flask(__name__, template_folder='views')
app.secret_key = 'chave-secreta-dev'
# variáveis com dois (_) são variáveis de ambientes no python
# __name_ representa o nome da aplicação

# Passando o nome do banco para o Flask
app.config['DATABASE_NAME'] = DB_NAME
# Passando o endereço do banco para o Flask=SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root@localhost:3306/{DB_NAME}'

# Enviando a variável app para as rotas
routes.init_app(app)

# Iniciando o servidor na porta 5000
if __name__ == '__main__':
    # Conectando-se ao MYSQL para criar o banco de dados
    # Passando os dados de conexao
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 charset='utf8mb4',
                                 port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
    # Tentando a conexão
    try:
        with connection.cursor() as cursor:
            # Enviando a QUERY para criar o banco
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')
            print("O banco de dados está criado!")

    except Exception as error:
        print(f"Ocorreu um erro ao criar o banco de dados! {error}")
        # Fechando a conexão
    finally:
        connection.close()

    # Incializando o FLASK-SQLALCHEMY
    db.init_app(app=app)
    # Enviando a requisição para criar as tabelas
    with app.test_request_context():
        db.create_all()

    # Inicialidando o servidor:
    # verificando se o arquivo gravado em __name__ é o arquivo principal
    app.run(port=5000, debug=True)
    # o método .run() inicia o servidor
