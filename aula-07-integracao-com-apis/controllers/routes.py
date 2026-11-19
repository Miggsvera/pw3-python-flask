# Importando o flask para a aplicação
from flask import render_template, request, redirect, url_for, session
# Criando a função principal para a inicializar as rotas
# Importando o modo de Games
from models.database import Game, db, Console, Usuario
# Importando a biblioteca Werkzeug
from werkzeug.security import check_password_hash, generate_password_hash

import urllib.request #Envia requisições para uma URL(endereço online)
import json   #Converte dados de dicionário para JSON e vice-versa

#Criando a função principal para inicializar as rotas



def init_app(app):
    # Funlão de middleware
    @app.before_request
    def check_auth():
        # Rotas que não precisam de autenticação
        rotasPermitidas = ['home', 'login', 'cadastro', 'static']

        # Se a rota atual não requer autenticação
        if request.endpoint in rotasPermitidas:
            # Libera o acesso
            return
        # Se o usuário estiver tentando acessar uma rota protegida sem estas autenticado
        if 'usuario_id' not in session:
            # Redireciona para a página de login
            return redirect(url_for('login'))
    # Variáveis Globais
    listaConsoles = ['Playstation 5', 'Xbox One',
                     'Super Nintendo', 'Atari', '3DS']
    listaGames = [{'titulo': 'CS-GO', 'ano': 2012,
                   'categoria': 'FPS Online', 'plataforma': 'PC(Windows)'}]

    # Criando a rota principal do site

    @app.route('/')
    # def cria funções no python
    def home():
        return render_template('index.html')

    @app.route('/games')
    def games():
        # criando variáveis para a rota de games
        titulo = "Portal 2"
        ano = 2011
        categoria = "Puzzle"
        # Lista de Jogadores(uma lista é um vetor/array)
        jogadores = ['Marcos', 'Richard', 'Miguel', 'Renato', 'Pedro']

        # Enviando categorias para html
        return render_template('games.html',
                               titulo=titulo,
                               ano=ano,
                               categoria=categoria,
                               jogadores=jogadores)

    @app.route('/consoles', methods=['GET', 'POST'])
    def consoles():
        # Criando um objeto
        console = {"Nome": "Playstation 2",
                   "Fabricante": "Sony",
                   "Ano": 2000}

        # Recebendo o valor do formulário
        if request.method == 'POST':
            if request.form.get('novoConsole'):
                listaConsoles.append(request.form.get('novoConsole'))

        return render_template('consoles.html',
                               console=console,
                               listaConsoles=listaConsoles)

    # Rota para cadastrar o jogo
    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        # Recebendo os dados do formulário e enviando para página
        # Verificando se a requisição od usuário é do tipo POST
        if request.method == 'POST':
            # Aqui ele irá gravar os dados na lista de jogos
            listaGames.append({'titulo': request.form.get('titulo'), 'ano': request.form.get
                               ('ano'), 'categoria': request.form.get('categoria'), 'plataforma': request.form.get('plataforma')})
            # .append adiciona um item na lista
            # Aqui o usuário será redirecionado para a página
            return redirect(url_for('cadgames'))

        return render_template('cadgames.html',
                               listaGames=listaGames)

    # ROTA PARA O CRUD(estoque de jogos)
    @app.route('/estoque', methods=['GET', 'POST'])
    # adicionando o parâmetro id a rota
    @app.route('/estoque/delete/<int:id>')
    def estoque(id=None):

        # Verificandose o id foi passado para a rota
        if id:
            game = Game.query.get(id)  # seleciona o jogo
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for('estoque'))
        # Condição para verificar se o usuário está enviando uma requisação POST(cadastro)
        if request.method == 'POST':
            # Realiza o cadastro
            # Coletando os dados do formulário
            # Pega os dados do formulário e tranforma em um dicionário(objeto)
            dados = request.form.to_dict()
            # Enviando os dados para o model
            newgame = Game(dados['titulo'], dados['ano'], dados['categoria'],
                           dados['plataforma'], dados['preco'], dados['quantidade'])
            # Método do SQLAlchemy para gravar no banco
            db.session.add(newgame)
            # Configuração
            db.session.commit()
            return redirect(url_for('estoque'))
        # SECIONANDO TODOS OS JOGOS DA TABELA
        games = Game.query.all()
        return render_template('estoque.html', games=games)

    @app.route('/estoque_console', methods=['GET', 'POST'])
    def estoque_console():
        if request.method == 'POST':
            dados = request.form.to_dict()
            newconsole = Console(
                dados['nome'], dados['fabricante'], dados['ano'], dados['preco'], dados['quantidade'])
            db.session.add(newconsole)
            db.session.commit()
            return redirect(url_for('estoque_console'))
        consoles = Console.query.all()
        return render_template('estoque_console.html', consoles=consoles)

    @app.route('/estoque/editar/<int:id>', methods=['GET', 'POST'])
    def editar(id):
        # Selecionando o jogo no banco pelo id
        game = Game.query.get(id)
        # Verificando se a requisição é POST
        if request.method == 'POST':
            dados_form = request.form.to_dict()
            # Alterando os dados do jogo
            game.titulo = dados_form['titulo']
            game.ano = dados_form['ano']
            game.categoria = dados_form['categoria']
            game.plataforma = dados_form['plataforma']
            game.preco = dados_form['preco']
            game.quantidade = dados_form['quantidade']
            db.session.commit()
            return redirect(url_for('estoque'))
        return render_template('editGame.html', game=game)
    #ROTA DE CADASTRO
    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro():
        if request.method == 'POST':
            # Coleta os dados do form
            email = request.form['email']
            senha = request.form['senha']
            #Gerando o hash de senha(criptografia)
            senha_com_hash = generate_password_hash(senha, method='scrypt')
            #Enviado dados no banco 
            novo_usuario = Usuario(email=email, senha=senha_com_hash)
            #Gravando no banco 
            db.session.add(novo_usuario)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('cadastro.html')
    
    #ROTA DE LOGIN
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            senha = request.form['senha']
            usuario = Usuario.query.filter_by(email=email).first()

            if usuario and check_password_hash(usuario.senha, senha):
                session['usuario_id'] = usuario.id
                return redirect(url_for('home'))

            return render_template('login.html', erro='E-mail ou senha inválidos.'), 401

        return render_template('login.html')
    
    # Rota do consumo da API
    @app.route('/apigames', methods=['GET', 'POST'])
    @app.route('/apigames/<int:id>', methods=['GET', 'POST'])
    def apigames(id=None):
        # Variável que armazena a URL da API
        url = "https://www.freetogame.com/api/games"
        
        req = urllib.request.urlopen(url)
        
        dados = req.read()
        #Convertendo a resposta da API de JSON para DICIONÁRIO 
        listaJogos = json.loads(dados)
        
        # VERIFICANDO SE FOR PASSADO UMA ID PARA ROTA   
        if id:
            jogoInfo = []
            for jogo in listaJogos:
                # VERIFIQUE SE O ID CORRESPONDE
                if jogo['id'] == id:
                    jogoInfo = jogo
                    # Interrompendo o for
                    break 
            if jogoInfo:
                return render_template('jogoInfo.html', jogoInfo=jogoInfo)
            else:
                return f'Game com ID {id} não encontrado!'
        else:
            return render_template('apigames.html', listaJogos=listaJogos)

    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        # Destruindo a sessão do usuário
        session.clear()
        return redirect(url_for('home'))