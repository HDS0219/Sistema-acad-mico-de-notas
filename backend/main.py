import os
import sqlite3

# Caminho para o banco de dados
caminho = os.path.dirname(__file__)
nome_arquivo = os.path.join(caminho, "notas.db")

def calcular_media(*notas):
    return sum(notas) / len(notas)

def criar_tabela():
    with sqlite3.connect(nome_arquivo) as conexao:
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
            conexao.execute(sql)
            print("Tabela 'notas' criada ou já existente.")
        except sqlite3.Error as e:
            print(f"Erro ao criar tabela: {e}")

def executar_query(conexao, sql, dados=None):
    try:
        with conexao:
            cursor = conexao.cursor()
            if dados:
                cursor.execute(sql, dados)
            else:
                cursor.execute(sql)
            print("Query executada com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao executar a query: {e}")

def consultar(conexao, sql, dados=None):
    try:
        cursor = conexao.cursor()
        if dados:
            cursor.execute(sql, dados)
        else:
            cursor.execute(sql)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao realizar a consulta: {e}")
        return []

def menu():
    with sqlite3.connect(nome_arquivo) as conexao:
        while True:
            print("\nSistema de Notas")
            print("1. Inserir Nota")
            print("2. Deletar Nota")
            print("3. Atualizar Nota")
            print("4. Consultar Nota")
            print("5. Sair")

            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                menu_inserir(conexao)
            elif opcao == '2':
                menu_deletar(conexao)
            elif opcao == '3':
                menu_atualizar(conexao)
            elif opcao == '4':
                consultar_matricula(conexao)
            elif opcao == '5':
                print("Saindo...")
                break
            else:
                print("Opção inválida, tente novamente.")

def menu_inserir(conexao):
    aluno = input("Nome do aluno: ")
    disciplina = input("Disciplina: ")
    notas = [float(input(f"Nota {i + 1}: ")) for i in range(4)]
    media = calcular_media(*notas)

    inserir_nota(conexao, aluno, disciplina, *notas, media)

def menu_deletar(conexao):
    nome = input("Digite o nome do aluno para deletar: ")
    resultado = consultar(conexao, "SELECT * FROM notas WHERE aluno = ?", (nome,))

    if resultado:
        confirmacao = input(f"Tem certeza que deseja deletar as notas de {nome}? (s/n): ").lower()
        if confirmacao == 's':
            executar_query(conexao, "DELETE FROM notas WHERE aluno = ?", (nome,))
            print(f"Notas de {nome} deletadas com sucesso!")
        else:
            print("Operação cancelada.")
    else:
        print("Aluno não encontrado.")

def menu_atualizar(conexao):
    nome = input("Digite o nome do aluno para atualizar: ")
    resultado = consultar(conexao, "SELECT * FROM notas WHERE aluno = ?", (nome,))

    if resultado:
        notas_atuais = resultado[0][3:7]
        print(f"Notas atuais de {nome}: {notas_atuais} (média: {resultado[0][7]})")

        novas_notas = [float(input(f"Nova Nota {i + 1}: ")) for i in range(4)]
        media = calcular_media(*novas_notas)

        sql_update = '''
        UPDATE notas
        SET nota1 = ?, nota2 = ?, nota3 = ?, nota4 = ?, media = ?
        WHERE aluno = ?;
        '''
        executar_query(conexao, sql_update, (*novas_notas, media, nome))
        print(f"Notas de {nome} atualizadas com sucesso!")
    else:
        print("Aluno não encontrado.")

def consultar_matricula(conexao):
    nome = input("Digite o nome do aluno para consultar: ")
    resultados = consultar(conexao, "SELECT * FROM notas WHERE aluno = ?", (nome,))

    if resultados:
        for resultado in resultados:
            print(f"Aluno: {resultado[1]}, Disciplina: {resultado[2]}, Notas: {resultado[3:7]}, Média: {resultado[7]}")
    else:
        print("Nenhuma nota encontrada para o aluno.")

def inserir_nota(conexao, aluno, disciplina, nota1, nota2, nota3, nota4, media):
    sql = '''
    INSERT INTO notas (aluno, disciplina, nota1, nota2, nota3, nota4, media)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    '''
    executar_query(conexao, sql, (aluno, disciplina, nota1, nota2, nota3, nota4, media))

if __name__ == "__main__":
    criar_tabela()
    menu()
