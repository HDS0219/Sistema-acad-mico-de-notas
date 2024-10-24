import os
import sqlite3

# Caminho para o banco de dados
caminho = os.path.dirname(__file__)
nomeArquivo = os.path.join(caminho, "..", "notas.db")

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
            media REAL,
            passou BOOLEAN
        );
        '''
        cursor = conexao.cursor()
        cursor.execute(sql)
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao criar tabela: {e}")

def conexaoBanco():
    try:
        conexao = sqlite3.connect(nomeArquivo)
        return conexao
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def inserir_nota(conexao, aluno, disciplina, nota1, nota2, nota3, nota4):
    media = (nota1 + nota2 + nota3 + nota4) / 4
    passou = media >= 6
    try:
        sql = '''
        INSERT INTO notas (aluno, disciplina, nota1, nota2, nota3, nota4, media, passou)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        '''
        cursor = conexao.cursor()
        cursor.execute(sql, (aluno, disciplina, nota1, nota2, nota3, nota4, media, passou))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inserir notas: {e}")

def consultar(conexao, aluno):
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM notas WHERE aluno = ?", (aluno,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao realizar a consulta: {e}")
        return []

def atualizar_nota(conexao, aluno, nota1, nota2, nota3, nota4):
    media = (nota1 + nota2 + nota3 + nota4) / 4
    passou = media >= 6
    try:
        sql = '''
        UPDATE notas
        SET nota1 = ?, nota2 = ?, nota3 = ?, nota4 = ?, media = ?, passou = ?
        WHERE aluno = ?;
        '''
        cursor = conexao.cursor()
        cursor.execute(sql, (nota1, nota2, nota3, nota4, media, passou, aluno))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao atualizar notas: {e}")

def deletar_nota(conexao, aluno):
    try:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM notas WHERE aluno = ?", (aluno,))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao deletar notas: {e}")
