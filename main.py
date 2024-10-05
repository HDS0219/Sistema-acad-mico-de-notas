import os
import sqlite3
from sqlite3 import Error

from select import error

caminho = os.path.dirname(__file__)
nomeArquivo = os.path.join(caminho, "notas.db")

def criar_tabela(conexao):
    try:
        sql = '''
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno TEXT NOT NULL,
            disciplina TEXT NOT NULL,
            nota1 REAL NOT NULL,
            nota2 REAL NOT NULL,
            nota3 REAL NOT NULL,
            nota4 REAL NOT NULL,
            media REAL
        );
        '''
        cursor = conexao.cursor()
        cursor.execute(sql)
        conexao.commit()
    except Error as e:
        print(f"Erro ao criar tabela: {e}")


def conexaoBanco():
    conexao = None
    try:
        conexao = sqlite3.connect(nomeArquivo)
        print("Conectado ao banco de dados com sucesso!")
    except Error as e:
        print(f"Erro ao conectar ao banco de dados... {e}")

def query(conexao, sql, dados=None):
    ...

def consultar(conexao, sql, dados=None):
    ...

#por enquanto foi adicionado no terminal o banco de dados.
def menu():
    ...

def menuInserir():
    ...

def menuDeletar():
    ...

def menuAtualizar():
    ...

def consultarMatricula():
    ...

def inserir_nota(conexao, aluno, disciplina, nota1, nota2, nota3, nota4):
    media = (nota1 + nota2 + nota3 + nota4) / 4
    try:
        sql = '''
        INSERT INTO notas (aluno, disciplina, nota1, nota2, nota3, nota4, media)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        '''
        cursor = conexao.cursor()
        cursor.execute(sql, (aluno, disciplina, nota1, nota2, nota3, nota4, media))
        conexao.commit()
    except Error as e:
        print(f"Erro ao inserir notas: {e}")

