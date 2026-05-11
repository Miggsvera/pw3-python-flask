# Importando o Flask-SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
# Carregando o SqlAlchemy em uma variável chamada db
db = SQLAlchemy()

# Criando uma classe para representar a entidade Game no banco de dados
class Game(db.Model):
    # definindo atributos (colnunas) da tabela Game
    # Schema
    id = db.Column(db.Integer, primary_key=True)  # Coluna de ID, chave primária
    titulo = db.Column(db.String(150))  # Coluna de título, string de até 150 caracteres
    ano = db.Column(db.Integer)  # Coluna de ano, inteiro
    categoria = db.Column(db.String(150))  # Coluna de categoria, string de até 150 caracteres
    plataforma = db.Column(db.String(150))  # Coluna de plataforma, string de até 150 caracteres
    preco = db.Column(db.Float)  # Coluna de preço, float
    quantidade = db.Column(db.Integer)  # Coluna de quantidade, inteiro
    
    # Inicializando as variáveis da classe Game (método construtor)
    def __init__(self, titulo, ano, categoria, preco, quantidade, plataforma):
        self.titulo = titulo
        self.ano = ano
        self.categoria = categoria
        self.preco = preco
        self.quantidade = quantidade
        self.plataforma = plataforma
        
class Console(db.Model):
    # definindo atributos (colnunas) da tabela Game
    # Schema
    id = db.Column(db.Integer, primary_key=True)  # Coluna de ID, chave primária
    nome = db.Column(db.String(150))  # Coluna de título, string de até 150 caracteres
    fabricante = db.Column(db.String(150))  # Coluna de fabricante, string de até 150 caracteres
    ano = db.Column(db.Integer)  # Coluna de ano, inteiro
    preco = db.Column(db.Float)  # Coluna de preço, float
    quantidade = db.Column(db.Integer)  # Coluna de quantidade, inteiro
    
    # Inicializando as variáveis da classe Game (método construtor)
    def __init__(self, nome, fabricante, ano, preco, quantidade):
        self.nome = nome
        self.fabricante = fabricante
        self.ano = ano
        self.preco = preco
        self.quantidade = quantidade