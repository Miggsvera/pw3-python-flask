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
    #criando variáveis para a rota de games
    titulo = "Portal 2"
    ano = 2011
    categoria = "Puzzle"
    #Lista de Jogadores(uma lista é um vetor/array)
    jogadores = ['Marcos','Richard','Miguel','Renato','Pedro']
    
    #Enviando categorias para html
    return render_template('games.html',
                           titulo = titulo,
                           ano=ano,
                           categoria=categoria,
                           jogadores=jogadores)

@app.route('/consoles')
def consoles():
    # Criando um objeto
    console = {"Nome": "Playstation 2",
               "Fabricante": "Sony",
               "Ano": 2000}
    return render_template('consoles.html',
                           console= console)


# Iniciando o servidor na porta 5000
if __name__ == '__main__':
# verificando se o arquivo gravado em __name__ é o arquivo principal    
    app.run(port=5000, debug =True)
# o método .run() inicia o servidor 
