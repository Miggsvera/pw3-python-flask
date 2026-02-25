# Comentário no python
# Importando o flask para a aplicação
from flask import Flask, render_template   # do pacote do flask, importe a classe Flask
#carregando o Flask na variável "app"
#declarando variável no python: nome = "..."
app = Flask(__name__, template_folder ='views')
# variáveis com dois (_) são variáveis de ambientes no python 
# __name_ representa o nome da aplicação

# Criando a rota principal do site
@app.route('/')
# def cria funções no python
def home():
    return render_template('index.html')

@app.route('/games')
def games():
    return render_template('games.html')

@app.route('/consoles')
def consoles():
    return render_template('consoles.html')


# Iniciando o servidor na porta 5000
if __name__ == '__main__':
# verificando se o arquivo gravado em __name__ é o arquivo principal    
    app.run(port=5000, debug =True)
# o método .run() inicia o servidor 
