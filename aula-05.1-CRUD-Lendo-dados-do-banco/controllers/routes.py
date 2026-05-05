# Importando o flask para a aplicação
from flask import render_template, request, redirect, url_for
# Importando o model de games
from models.database import Console, Game, db  # do pacote do flask, importe a classe Flask



# Criado a função principal para inicializar as rotas
def init_app(app):
    # VARIÁVEIS GLOBAIS
    listaConsoles = ['Playstation 5','Xbox One','Super Nintendo','Atari1','3DS']
    
    listaGames = [{'titulo' : 'CS-GO', 'ano' : 2012, 'categoria' : 'FPS Online', 'plataforma' : 'PC (Windows)'}]
    
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
        
    # Rota para cadastrar jogo
    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        #Verificando se a requisição do usuario é do metodo post
        # Recebendo os dados do formulário e enviando para página
        if request.method == 'POST' :
            listaGames.append({'titulo' : request.form.get('titulo'), 'ano' : request.form.get('ano'), 'categoria' : request.form.get('categoria'), 'plataforma' : request.form.get('plataforma')})
            #Aqui o usuário será redirecionado novamente para a página
            return redirect(url_for('cadgames'))
            
        return render_template('cadgames.html', 
                               listaGames = listaGames)
    
    # Rota para o crud (estoque de jogos)
    @app.route('/estoque', methods=['GET', 'POST'])
    def estoque():
        # Condição para verificar se o usuário está enviando uma requisição do tipo POST(cadastro de novo jogo)
        if request.method == 'POST':
            #Realiza o cadastro
            #Coletando os dados do formulário
            #Pega os dados do formulário e transforma em um dicionário (objeto)
            dados = request.form.to_dict()
            # Enviando os dados para o Model
            newgame = Game(
                dados['titulo'],
                dados['ano'],
                dados['categoria'],
                dados['plataforma'],
                dados['preco'],
                dados['quantidade']
            )
            # Método do SQLAlchemy para adicionar o novo jogo no banco de dados
            db.session.add(newgame)
            # Confirmação
            db.session.commit()
            return redirect(url_for('estoque'))
        # Selecionando todos os jogos da tabela
        games = Game.query.all()
        return render_template('estoque.html', games=games)
    
    @app.route('/estoque_consoles', methods=['GET', 'POST'])
    def estoque_consoles():
        if request.method == 'POST':
            #Realiza o cadastro
            #Coletando os dados do formulário
            #Pega os dados do formulário e transforma em um dicionário (objeto)
            dados = request.form.to_dict()
            # Enviando os dados para o Model
            newconsole = Console(
                dados['nome'],
                dados['fabricante'],
                dados['ano'],
                dados['preco'],
                dados['quantidade']
            )
            # Método do SQLAlchemy para adicionar o novo console no banco de dados
            db.session.add(newconsole)
            # Confirmação
            db.session.commit()
            return redirect(url_for('estoque_consoles'))
        # Selecionando todos os consoles da tabela
        consoles = Console.query.all()
        return render_template('estoque_consoles.html', consoles=consoles)