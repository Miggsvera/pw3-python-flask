# Importando o flask para a aplicação
from flask import render_template, request, redirect, url_for

# Dados em memória da aplicação
lista_autores = [
    {'nome': 'Vagabond', 'fabricante': 'Takehiko Inoue', 'ano': 1998},
    {'nome': 'Berserk', 'fabricante': 'Kentaro Miura', 'ano': 1989},
    {'nome': 'Monster', 'fabricante': 'Naoki Urasawa', 'ano': 1994},
    {'nome': 'Slam Dunk', 'fabricante': 'Takehiko Inoue', 'ano': 1990},
    {'nome': 'Oyasumi Punpun', 'fabricante': 'Inio Asano', 'ano': 2007}
]

lista_mangas = [
    {
        'titulo': 'One Piece',
        'ano': 1997,
        'categoria': 'Shonen',
        'plataforma': 'Panini'
    }
]


def listar_autores():
    return lista_autores


def adicionar_autor(nome, fabricante, ano):
    if not nome or not fabricante or not ano:
        return

    lista_autores.append({'nome': nome, 'fabricante': fabricante, 'ano': ano})


def listar_mangas():
    return lista_mangas


def adicionar_manga(titulo, ano, categoria, plataforma):
    if not titulo or not ano or not categoria or not plataforma:
        return

    lista_mangas.append(
        {
            'titulo': titulo,
            'ano': ano,
            'categoria': categoria,
            'plataforma': plataforma
        }
    )


# Criado a função principal para inicializar as rotas
def init_app(app):
    # Criando a rota principal do site
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/mangas')
    def mangas():
        # criando variáveis para a rota de mangas
        titulo = "Vinland Saga"
        ano = 2005
        categoria = "Seinen Historico"
        # Lista de personagens
        jogadores = ['Thorfinn', 'Askeladd', 'Canute', 'Thors', 'Einar']

        # Enviando categorias para html
        return render_template(
            'mangas.html',
            titulo=titulo,
            ano=ano,
            categoria=categoria,
            jogadores=jogadores
        )

    @app.route('/autores')
    def autores():
        # Criando um objeto de manga em destaque
        console = {"Obra": "20th Century Boys", "Autor": "Naoki Urasawa", "Ano": 1999}

        return render_template(
            'autores.html',
            console=console,
            listaAutores=listar_autores()
        )

    # Rota para cadastrar manga
    @app.route('/cadmangas', methods=['GET', 'POST'])
    def cadmangas():
        if request.method == 'POST':
            adicionar_manga(
                request.form.get('titulo'),
                request.form.get('ano'),
                request.form.get('categoria'),
                request.form.get('plataforma')
            )
            return redirect(url_for('cadmangas'))

        return render_template('cadmangas.html', listaMangas=listar_mangas())

    # Rota para cadastrar obra/autoria
    @app.route('/cadautores', methods=['GET', 'POST'])
    def cadautores():
        if request.method == 'POST':
            adicionar_autor(
                request.form.get('nome'),
                request.form.get('fabricante'),
                request.form.get('ano')
            )
            return redirect(url_for('cadautores'))

        return render_template('cadautores.html', listaAutores=listar_autores())