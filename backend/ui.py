import tkinter as tk
from tkinter import messagebox, ttk
from backend import *

class SistemaAcademico:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Acadêmico de Notas")
        self.root.geometry("600x500")

        # Conectar ao banco de dados
        self.conexao = conexaoBanco()
        if self.conexao:
            criar_tabela(self.conexao)

        # Interface
        self.create_widgets()

    def create_widgets(self):
        # Labels e Entradas
        tk.Label(self.root, text="Nome do Aluno:").grid(row=0, column=0, padx=5, pady=3, sticky="w")
        self.aluno_entry = tk.Entry(self.root)
        self.aluno_entry.grid(row=0, column=1, padx=5, pady=3)

        tk.Label(self.root, text="Disciplina:").grid(row=1, column=0, padx=5, pady=3, sticky="w")
        self.disciplina_combo = ttk.Combobox(self.root, values=["Português", "Matemática", "História", "Geografia", "Química", "Física", "Biologia", "Filosofia"], state="readonly")
        self.disciplina_combo.grid(row=1, column=1, padx=5, pady=3)
        self.disciplina_combo.current(0)

        tk.Label(self.root, text="Nota 1:").grid(row=2, column=0, padx=5, pady=3, sticky="w")
        self.nota1_entry = tk.Entry(self.root)
        self.nota1_entry.grid(row=2, column=1, padx=5, pady=3)

        tk.Label(self.root, text="Nota 2:").grid(row=3, column=0, padx=5, pady=3, sticky="w")
        self.nota2_entry = tk.Entry(self.root)
        self.nota2_entry.grid(row=3, column=1, padx=5, pady=3)

        tk.Label(self.root, text="Nota 3:").grid(row=4, column=0, padx=5, pady=3, sticky="w")
        self.nota3_entry = tk.Entry(self.root)
        self.nota3_entry.grid(row=4, column=1, padx=5, pady=3)

        tk.Label(self.root, text="Nota 4:").grid(row=5, column=0, padx=5, pady=3, sticky="w")
        self.nota4_entry = tk.Entry(self.root)
        self.nota4_entry.grid(row=5, column=1, padx=5, pady=3)

        # Botões com menos espaçamento
        tk.Button(self.root, text="Inserir Notas", command=self.inserir_notas).grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        tk.Button(self.root, text="Consultar Notas", command=self.consultar_notas).grid(row=7, column=0, columnspan=2, padx=5, pady=5)
        tk.Button(self.root, text="Atualizar Notas", command=self.atualizar_notas).grid(row=8, column=0, columnspan=2, padx=5, pady=5)
        tk.Button(self.root, text="Deletar Notas", command=self.deletar_notas).grid(row=9, column=0, columnspan=2, padx=5, pady=5)

        # Tabela para exibir todos os alunos e suas notas
        self.tabela = ttk.Treeview(self.root, columns=("Aluno", "Disciplina", "Nota1", "Nota2", "Nota3", "Nota4", "Média", "Status"), show="headings")
        self.tabela.grid(row=10, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Cabeçalhos da tabela
        self.tabela.heading("Aluno", text="Aluno")
        self.tabela.heading("Disciplina", text="Disciplina")
        self.tabela.heading("Nota1", text="Nota 1")
        self.tabela.heading("Nota2", text="Nota 2")
        self.tabela.heading("Nota3", text="Nota 3")
        self.tabela.heading("Nota4", text="Nota 4")
        self.tabela.heading("Média", text="Média")
        self.tabela.heading("Status", text="Status")

        # Ajuste nas colunas da tabela
        for col in self.tabela["columns"]:
            self.tabela.column(col, width=70, anchor="center")

        self.carregar_dados_tabela()  # Carregar dados ao iniciar

    def inserir_notas(self):
        aluno = self.aluno_entry.get()
        disciplina = self.disciplina_combo.get()  # Obtém a disciplina selecionada
        nota1 = float(self.nota1_entry.get())
        nota2 = float(self.nota2_entry.get())
        nota3 = float(self.nota3_entry.get())
        nota4 = float(self.nota4_entry.get())
        inserir_nota(self.conexao, aluno, disciplina, nota1, nota2, nota3, nota4)
        messagebox.showinfo("Sucesso", "Notas inseridas com sucesso!")
        self.carregar_dados_tabela()  # Atualizar tabela após inserção

    def consultar_notas(self):
        aluno = self.aluno_entry.get()
        resultado = consultar(self.conexao, aluno)
        if resultado:
            notas = resultado[0][3:7]
            media = resultado[0][7]
            passou = resultado[0][8]
            status = "Aprovado" if passou else "Reprovado"
            messagebox.showinfo("Consulta", f"Notas: {notas}\nMédia: {media}\nStatus: {status}")
        else:
            messagebox.showerror("Erro", "Aluno não encontrado.")

    def atualizar_notas(self):
        aluno = self.aluno_entry.get()
        nota1 = float(self.nota1_entry.get())
        nota2 = float(self.nota2_entry.get())
        nota3 = float(self.nota3_entry.get())
        nota4 = float(self.nota4_entry.get())
        atualizar_nota(self.conexao, aluno, nota1, nota2, nota3, nota4)
        messagebox.showinfo("Sucesso", "Notas atualizadas com sucesso!")
        self.carregar_dados_tabela()  # Atualizar tabela após atualização

    def deletar_notas(self):
        aluno = self.aluno_entry.get()
        deletar_nota(self.conexao, aluno)
        messagebox.showinfo("Sucesso", "Notas deletadas com sucesso!")
        self.carregar_dados_tabela()  # Atualizar tabela após exclusão

    def carregar_dados_tabela(self):
        # Limpar tabela antes de carregar novos dados
        for row in self.tabela.get_children():
            self.tabela.delete(row)

        # Carregar dados do banco de dados
        cursor = self.conexao.cursor()
        cursor.execute("SELECT aluno, disciplina, nota1, nota2, nota3, nota4, media, passou FROM notas")
        for linha in cursor.fetchall():
            aluno, disciplina, nota1, nota2, nota3, nota4, media, passou = linha
            status = "Aprovado" if passou else "Reprovado"
            self.tabela.insert("", "end", values=(aluno, disciplina, nota1, nota2, nota3, nota4, media, status))

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaAcademico(root)
    root.mainloop()
# Achei que Swing do java era complicado... ambos são.