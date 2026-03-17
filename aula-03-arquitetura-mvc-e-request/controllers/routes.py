# Importando o flask para a aplicação
from flask import render_template, request   # do pacote do flask, importe a classe Flask



# Criado a função principal para inicializar as rotas
def init_app(app):
    # VARIÁVEIS GLOBAIS
    listaConsoles = ['Playstation 5','Xbox One','Super Nintendo','Atari1','3DS']
    
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

    @app.route('/consoles', methods=['GET', 'POST'])
    def consoles():
        # Criando um objeto
        console = {"Nome": "Playstation 2",
                "Fabricante": "Sony",
                "Ano": 2000}
        
        
        
        #Recebendo o valor do formulário
        if request.method == 'POST':
            if request.form.get('novoConsole'):
                listaConsoles.append(request.form.get('novoConsole'))
        
        return render_template('consoles.html',
                            console= console,
                            listaconsoles=listaConsoles)