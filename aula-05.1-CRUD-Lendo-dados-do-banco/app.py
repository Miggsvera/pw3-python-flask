# Comentário no python
# Importando o flask para a aplicação
from flask import Flask, render_template
# Importando PYMSQL
import pymysql
# Importando o SQLAlchemy e o model
from models.database import db, Game, Console

#Definindo um nome para o banco
DB_NAME = 'thegames'

from controllers import routes
# do pacote do flask, importe a classe Flask
#carregando o Flask na variável "app"
#declarando variável no python: nome = "..."
app = Flask(__name__, template_folder ='views')
# variáveis com dois (_) são variáveis de ambientes no python 
# __name_ representa o nome da aplicação




# Passando o nome do banco para o flask
app.config['DATABASE_NAME'] = DB_NAME
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root@localhost/{DB_NAME}'

# Enviando a variável app para as rotas
routes.init_app(app)



# Iniciando o servidor na porta 5000
if __name__ == '__main__':
    # Conectando-se ao MYSQL para criar o banco de dados
    # Passando os dados de conexão
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            # Enviando a QUERY para criar o banco de dados
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            print("O banco de dados foi criado com sucesso!")
    except Exception as error:
        print(f"Erro ao criar o banco de dados: {error}")
    # Fechando a conexão com o banco de dados
    finally:
        connection.close()
        
    #Inicializando o SQLAlchemy com a aplicação Flask
    db.init_app(app=app)
    with app.test_request_context():
        # Criando as tabelas no banco de dados
        db.create_all()
        print("As tabelas foram criadas com sucesso!")
            
    # Iniciando o servidor na porta 5000
    app.run(debug=True, port=5000)
