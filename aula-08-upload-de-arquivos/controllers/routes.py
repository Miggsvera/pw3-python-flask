# Importando o Flask para a aplicação
from fileinput import filename

from flask import flash, render_template, request, redirect, url_for

# Importando o Model de Games
from models.database import Game, db, Console, Usuario

# Importando a biblioteca Werkzeug
from werkzeug.security import generate_password_hash

# Importando a biblioteca URLLIB
import urllib.request  # Permite enviar requisições para uma URL

# Importando a biblioteca JSON
import json  # Converte dados de dicionário para JSON e vice-versa

# Importando a biblioteca OS (Manipula o Sitema Operacional)
import os

# Importando a biblioteca UUID (Identificador único universal)
import uuid


# Criando a função principal para inicializar as rotas


def init_app(app):
    # VARIÁVEIS GLOBAIS
    listaConsoles = ["Playstation 5", "Xbox One", "Super Nintendo", "Atari", "3DS"]

    listaGames = [
        {
            "titulo": "CS-GO",
            "ano": 2012,
            "categoria": "FPS Online",
            "plataforma": "PC (Windows)",
        }
    ]

    # CRIANDO A ROTA PRINCIPAL DO SITE
    @app.route("/")
    # def cria funções no Python
    def home():
        return render_template("index.html")

    @app.route("/games")
    def games():
        # Criando variáveis para a rota de games
        titulo = "Portal 2"
        ano = 2011
        categoria = "Puzzle"
        # Lista de jogadores (uma lista é um vetor/array)
        jogadores = ["Marcos", "Richard", "Miguel", "Renato", "Pedro"]
        # Enviando as variáveis para o HTML
        return render_template(
            "games.html",
            titulo=titulo,
            ano=ano,
            categoria=categoria,
            jogadores=jogadores,
        )

    @app.route("/consoles", methods=["GET", "POST"])
    def consoles():
        # Criando um objeto
        console = {"Nome": "Playstation 2", "Fabricante": "Sony", "Ano": 2000}

        # Recendo o valor do formulário
        if request.method == "POST":
            if request.form.get("novoConsole"):
                listaConsoles.append(request.form.get("novoConsole"))

        return render_template(
            "consoles.html", console=console, listaConsoles=listaConsoles
        )

    # ROTA PARA CADASTRAR UM JOGO
    @app.route("/cadgames", methods=["GET", "POST"])
    def cadgames():

        # Recebendo os dados do formulário e enviando para página
        # Verificando se a requisição do usuário é do tipo POST
        if request.method == "POST":
            # Aqui ele irá gravar os dados na lista de jogos
            listaGames.append(
                {
                    "titulo": request.form.get("titulo"),
                    "ano": request.form.get("ano"),
                    "categoria": request.form.get("categoria"),
                    "plataforma": request.form.get("plataforma"),
                }
            )
            # Aqui o usuário será redirecionado novamente para a página
            return redirect(url_for("cadgames"))
        return render_template("cadgames.html", listaGames=listaGames)

    # ROTA PARA O CRUD (ESTOQUE DE JOGOS)
    @app.route("/estoque", methods=["GET", "POST"])
    # ADICIONANDO O PARÂMETRO ID A ROTA
    @app.route("/estoque/delete/<int:id>")
    def estoque(id=None):
        # VERIFICANDO SE O ID FOI PASSADO PARA ROTA
        if id:
            game = Game.query.get(id)  # SELECIONA O JOGO
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for("estoque"))

        # CONDIÇÃO PARA VERIFICAR SE O USUÁRIO ESTÁ ENVIANDO UMA REQUISIÇÃO POST (cadastro)
        if request.method == "POST":
            # REALIZA O CADASTRO
            # COLETANDO OS DADOS DO FORMULÁRIO
            # Pega os dados do formulário e transforma em um dicionário (objeto)
            dados = request.form.to_dict()
            # Enviando os dados para o Model
            newgame = Game(
                dados["titulo"],
                dados["ano"],
                dados["categoria"],
                dados["plataforma"],
                dados["preco"],
                dados["quantidade"],
            )
            # Método do SQLAlchemy para gravar no banco
            db.session.add(newgame)
            # Confirmação
            db.session.commit()
            return redirect(url_for("estoque"))
        # SELECIONANDO TODOS OS JOGOS DA TABELA
        games = Game.query.all()
        return render_template("estoque.html", games=games)

    @app.route("/estoque/editar/<int:id>", methods=["GET", "POST"])
    def editar(id):
        # Selecionando o jogo no banco pelo ID
        game = Game.query.get(id)
        # Verificando se a requisição é POST
        if request.method == "POST":
            dados_form = request.form.to_dict()
            # Alterando os dados do jogo
            game.titulo = dados_form["titulo"]
            game.ano = dados_form["ano"]
            game.categoria = dados_form["categoria"]
            game.plataforma = dados_form["plataforma"]
            game.preco = dados_form["preco"]
            game.quantidade = dados_form["quantidade"]
            db.session.commit()
            return redirect(url_for("estoque"))
        return render_template("editGame.html", game=game)

    # ROTA DE CADASTRO

    @app.route("/cadastro", methods=["GET", "POST"])
    def cadastro():
        if request.method == "POST":
            # COLETA OS DADOS DO FORMULÁRIO
            email = request.form["email"]
            senha = request.form["senha"]
            # GERANDO O HASH DE SENHA (CRIPTOGRAFIA)
            senha_com_hash = generate_password_hash(senha, method="scrypt")
            # ENVIANDO OS DADOS PARA O MODEL
            novo_usuario = Usuario(email=email, senha=senha_com_hash)
            # GRAVANDO NO BANCO
            db.session.add(novo_usuario)
            db.session.commit()
            return redirect(url_for("login"))
        return render_template("cadastro.html")

    # ROTA DE LOGIN
    @app.route("/login")
    def login():
        return render_template("login.html")

    # ROTA DE CONSUMO DA API
    @app.route("/apigames", methods=["GET", "POST"])
    # Recebendo o id como parâmetro
    @app.route("/apigames/<int:id>", methods=["GET", "POST"])
    def apigames(id=None):
        urlAPI = "https://www.freetogame.com/api/games"
        # Enviando uma REQUISIÇÃO para a API
        resposta = urllib.request.urlopen(urlAPI)
        # Lendo os dados
        dados = resposta.read()
        # Convertando dados de JSON para DICIONÁRIO
        listaJogos = json.loads(dados)
        # Verificando se a rota recebeu um id:
        if id:
            jogoInfo = []
            # Buscando o jogo na lista
            for jogo in listaJogos:
                if jogo["id"] == id:
                    jogoInfo = jogo
                    # Interrompendo o for
                    break
            # Se o jogo for encontrado
            if jogoInfo:
                return render_template("gameinfo.html", jogoInfo=jogoInfo)
            else:
                return f"Jogo com a ID {id} não foi encontrado."
        else:
            # Renderizando a página e enviando a lista de jogos
            return render_template("apigames.html", listaJogos=listaJogos)

    # ROTA DE UPLOAD DE ARQUIVOS (GALERIA)
    @app.route("/galeria", methods=["GET", "POST"])
    def galeria():

        # Definindo tipos de arquivos permitidos
        FILE_TYPES = set(['png', 'jpg', 'jpeg', 'gif', 'webp'])
        def arquivos_permitidos(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in FILE_TYPES
        
        # recebendo o arquivo enviado pelo usuário
        if request.method == "POST":
            # Caputa o arquivo do formulário
            file = request.files['file']
            # Enviando o arquivo para verificar se a extensão é permitida
            if not arquivos_permitidos(file.filename):
                flash("Tipo de arquivo não permitido. Apenas imagens são aceitas.", "danger")
                return redirect(request.url)
            # Se o tipo de arquivo for permitido, cria um nome aleatório para o arquivo
            filename = str(uuid.uuid4())
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # exibe mensagem de sucesso
            flash("Arquivo enviado com sucesso!", "success")
            return redirect(url_for('galeria'))

        return render_template("galeria.html")
