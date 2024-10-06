import os
import sqlite3

# Caminho para o banco de dados
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
    except sqlite3.Error as e:
        print(f"Erro ao criar tabela: {e}")

def conexaoBanco():
    conexao = None
    try:
        conexao = sqlite3.connect(nomeArquivo)
        print("Conectado ao banco de dados com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados... {e}")
    return conexao

def query(conexao, sql, dados=None):
    try:
        cursor = conexao.cursor()
        if dados:
            cursor.execute(sql, dados)
        else:
            cursor.execute(sql)
        conexao.commit()
        print("Query executada com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao executar a query... {e}")

def consultar(conexao, sql, dados=None):
    try:
        cursor = conexao.cursor()
        if dados:
            cursor.execute(sql, dados)
        else:
            cursor.execute(sql)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao realizar a consulta... {e}")
        return []

def menu(conexao):
    while True:
        print("\nSistema de Notas")
        print("1. Inserir Nota")
        print("2. Deletar Nota")
        print("3. Atualizar Nota")
        print("4. Consultar Nota")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            menuInserir(conexao)
        elif opcao == '2':
            menuDeletar(conexao)
        elif opcao == '3':
            menuAtualizar(conexao)
        elif opcao == '4':
            consultarMatricula(conexao)
        elif opcao == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente.")

def menuInserir(conexao):
    aluno = input("Nome do aluno: ")
    disciplina = input("Disciplina: ")
    nota1 = float(input("Nota 1: "))
    nota2 = float(input("Nota 2: "))
    nota3 = float(input("Nota 3: "))
    nota4 = float(input("Nota 4: "))

    inserir_nota(conexao, aluno, disciplina, nota1, nota2, nota3, nota4)

def menuDeletar(conexao):
    nome = input("Digite o nome do aluno para deletar: ")
    sql = "SELECT * FROM notas WHERE aluno = ?"
    resultado = consultar(conexao, sql, (nome,))

    if resultado:
        confirmacao = input(f"Tem certeza que deseja deletar as notas de {nome}? (s/n): ").lower()
        if confirmacao == 's':
            try:
                sql_delete = "DELETE FROM notas WHERE aluno = ?"
                query(conexao, sql_delete, (nome,))
                print(f"Notas de {nome} deletadas com sucesso!")
            except sqlite3.Error as e:
                print(f"Erro ao deletar as notas: {e}")
        else:
            print("Operação cancelada.")
    else:
        print("Aluno não encontrado.")

def menuAtualizar(conexao):
    nome = input("Digite o nome do aluno para atualizar: ")
    sql = "SELECT * FROM notas WHERE aluno = ?"
    resultado = consultar(conexao, sql, (nome,))

    if resultado:
        print(f"Notas atuais de {nome}: {resultado[0][3:7]} (média: {resultado[0][7]})")

        nota1 = float(input("Nova Nota 1: "))
        nota2 = float(input("Nova Nota 2: "))
        nota3 = float(input("Nova Nota 3: "))
        nota4 = float(input("Nova Nota 4: "))
        media = (nota1 + nota2 + nota3 + nota4) / 4

        try:
            sql_update = '''
            UPDATE notas
            SET nota1 = ?, nota2 = ?, nota3 = ?, nota4 = ?, media = ?
            WHERE aluno = ?;
            '''
            query(conexao, sql_update, (nota1, nota2, nota3, nota4, media, nome))
            print(f"Notas de {nome} atualizadas com sucesso!")
        except sqlite3.Error as e:
            print(f"Erro ao atualizar as notas: {e}")
    else:
        print("Aluno não encontrado.")

def consultarMatricula(conexao):
    nome = input("Digite o nome do aluno para consultar: ")
    sql = "SELECT * FROM notas WHERE aluno = ?"
    resultados = consultar(conexao, sql, (nome,))

    if resultados:
        for resultado in resultados:
            print(resultado)
    else:
        print("Nenhuma nota encontrada para o aluno.")

def inserir_nota(conexao, aluno, disciplina, nota1, nota2, nota3, nota4):
    media = (nota1 + nota2 + nota3 + nota4) / 4
    try:
        sql = '''
        INSERT INTO notas (aluno, disciplina, nota1, nota2, nota3, nota4, media)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        '''
        query(conexao, sql, (aluno, disciplina, nota1, nota2, nota3, nota4, media))
    except sqlite3.Error as e:
        print(f"Erro ao inserir notas: {e}")

if __name__ == "__main__":
    conexao = conexaoBanco()
    if conexao:
        criar_tabela(conexao)
        menu(conexao)
