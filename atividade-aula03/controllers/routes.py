# Importando o flask para a aplicação
from flask import render_template, request, redirect, url_for

# Dados em memória da aplicação
lista_autores = [
    {'obra': 'Vagabond', 'autor': 'Takehiko Inoue', 'ano': 1998},
    {'obra': 'Berserk', 'autor': 'Kentaro Miura', 'ano': 1989},
    {'obra': 'Monster', 'autor': 'Naoki Urasawa', 'ano': 1994},
    {'obra': 'Slam Dunk', 'autor': 'Takehiko Inoue', 'ano': 1990},
    {'obra': 'Oyasumi Punpun', 'autor': 'Inio Asano', 'ano': 2007}
]

lista_mangas = [
    {
        'titulo': 'One Piece',
        'ano': 1997,
        'genero': 'Shonen',
        'editora': 'Panini'
    }
]


def listar_autores():
    return lista_autores


def adicionar_autor(obra, autor, ano):
    if not obra or not autor or not ano:
        return

    lista_autores.append({'obra': obra, 'autor': autor, 'ano': ano})


def listar_mangas():
    return lista_mangas


def adicionar_manga(titulo, ano, genero, editora):
    if not titulo or not ano or not genero or not editora:
        return

    lista_mangas.append(
        {
            'titulo': titulo,
            'ano': ano,
            'genero': genero,
            'editora': editora
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
        genero = "Seinen Historico"
        # Lista de personagens em destaque
        personagens = ['Thorfinn', 'Askeladd', 'Canute', 'Thors', 'Einar']

        # Enviando categorias para html
        return render_template(
            'mangas.html',
            titulo=titulo,
            ano=ano,
            genero=genero,
            personagens=personagens
        )

    @app.route('/autores')
    def autores():
        # Criando um objeto de manga em destaque
        manga_destaque = {"Obra": "20th Century Boys", "Autor": "Naoki Urasawa", "Ano": 1999}

        return render_template(
            'autores.html',
            manga_destaque=manga_destaque,
            lista_autores=listar_autores()
        )

    # Rota para cadastrar manga
    @app.route('/cadmangas', methods=['GET', 'POST'])
    def cadmangas():
        if request.method == 'POST':
            adicionar_manga(
                request.form.get('titulo'),
                request.form.get('ano'),
                request.form.get('genero'),
                request.form.get('editora')
            )
            return redirect(url_for('cadmangas'))

        return render_template('cadmangas.html', lista_mangas=listar_mangas())

    # Rota para cadastrar obra/autoria
    @app.route('/cadautores', methods=['GET', 'POST'])
    def cadautores():
        if request.method == 'POST':
            adicionar_autor(
                request.form.get('obra'),
                request.form.get('autor'),
                request.form.get('ano')
            )
            return redirect(url_for('cadautores'))

        return render_template('cadautores.html', lista_autores=listar_autores())