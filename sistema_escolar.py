
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# 1. CONEXÃO COM O BANCO DE DADOS

def conectar():
    conexao = sqlite3.connect("alunos.db")

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            matricula TEXT NOT NULL,
            curso TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    conexao.commit()
    return conexao


# 2. CADASTRAR ALUNO

def cadastrar():
    nome = campo_nome.get()
    matricula = campo_matricula.get()
    curso = campo_curso.get()
    email = campo_email.get()

    if not all([nome, matricula, curso, email]):
        messagebox.showwarning("Atenção", "Preencha todos os campos!")
        return

    conexao = conectar()

    conexao.execute("""
        INSERT INTO alunos (nome, matricula, curso, email)
        VALUES (?, ?, ?, ?)
    """, (nome, matricula, curso, email))

    conexao.commit()
    conexao.close()

    messagebox.showinfo("Sucesso", "Aluno cadastrado!")

    limpar()
    listar()


# 3. CONSULTAR ALUNOS

def listar():
    for item in tabela.get_children():
        tabela.delete(item)

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM alunos")

    for aluno in cursor.fetchall():
        tabela.insert("", tk.END, values=aluno)

    conexao.close()


# 4. SELECIONAR ALUNO

def selecionar(event):
    selecionado = tabela.selection()

    if selecionado:
        dados = tabela.item(selecionado[0], "values")

        limpar()

        campo_nome.insert(0, dados[1])
        campo_matricula.insert(0, dados[2])
        campo_curso.insert(0, dados[3])
        campo_email.insert(0, dados[4])


# 5. ATUALIZAR ALUNO

def atualizar():
    selecionado = tabela.selection()

    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um aluno!")
        return

    dados = tabela.item(selecionado[0], "values")

    nome = campo_nome.get()
    matricula = campo_matricula.get()
    curso = campo_curso.get()
    email = campo_email.get()

    if not all([nome, matricula, curso, email]):
        messagebox.showwarning("Atenção", "Preencha todos os campos!")
        return

    conexao = conectar()

    conexao.execute("""
        UPDATE alunos
        SET nome=?, matricula=?, curso=?, email=?
        WHERE id=?
    """, (nome, matricula, curso, email, dados[0]))

    conexao.commit()
    conexao.close()

    messagebox.showinfo("Sucesso", "Aluno atualizado!")

    limpar()
    listar()


# 6. EXCLUIR ALUNO

def excluir():
    selecionado = tabela.selection()

    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um aluno!")
        return

    dados = tabela.item(selecionado[0], "values")

    confirmar = messagebox.askyesno(
        "Confirmação",
        "Deseja excluir este aluno?"
    )

    if confirmar:
        conexao = conectar()

        conexao.execute(
            "DELETE FROM alunos WHERE id=?",
            (dados[0],)
        )

        conexao.commit()
        conexao.close()

        limpar()
        listar()


# 7. LIMPAR CAMPOS

def limpar():
    campo_nome.delete(0, tk.END)
    campo_matricula.delete(0, tk.END)
    campo_curso.delete(0, tk.END)
    campo_email.delete(0, tk.END)


# 8. CRIAR INTERFACE GRÁFICA

janela = tk.Tk()
janela.title("Sistema de Cadastro de Alunos")
janela.geometry("850x600")

tk.Label(
    janela,
    text="CADASTRO DE ALUNOS",
    font=("Arial", 18, "bold")
).pack(pady=15)


# FORMULÁRIO

tk.Label(janela, text="Nome").pack()
campo_nome = tk.Entry(janela, width=50)
campo_nome.pack(pady=3)

tk.Label(janela, text="Matrícula").pack()
campo_matricula = tk.Entry(janela, width=50)
campo_matricula.pack(pady=3)

tk.Label(janela, text="Curso").pack()
campo_curso = tk.Entry(janela, width=50)
campo_curso.pack(pady=3)

tk.Label(janela, text="E-mail").pack()
campo_email = tk.Entry(janela, width=50)
campo_email.pack(pady=3)


# BOTÕES

frame = tk.Frame(janela)
frame.pack(pady=15)

tk.Button(
    frame,
    text="Cadastrar",
    command=cadastrar,
    width=12
).pack(side=tk.LEFT, padx=5)

tk.Button(
    frame,
    text="Atualizar",
    command=atualizar,
    width=12
).pack(side=tk.LEFT, padx=5)

tk.Button(
    frame,
    text="Excluir",
    command=excluir,
    width=12
).pack(side=tk.LEFT, padx=5)

tk.Button(
    frame,
    text="Limpar",
    command=limpar,
    width=12
).pack(side=tk.LEFT, padx=5)


# TABELA DE ALUNOS

tabela = ttk.Treeview(
    janela,
    columns=("ID", "Nome", "Matricula", "Curso", "Email"),
    show="headings"
)

tabela.heading("ID", text="ID")
tabela.heading("Nome", text="Nome")
tabela.heading("Matricula", text="Matrícula")
tabela.heading("Curso", text="Curso")
tabela.heading("Email", text="E-mail")

tabela.column("ID", width=40)
tabela.column("Nome", width=170)
tabela.column("Matricula", width=100)
tabela.column("Curso", width=150)
tabela.column("Email", width=200)

tabela.pack(pady=10, fill=tk.X, padx=10)

# EVENTO CORRIGIDO
tabela.bind("<<TreeviewSelect>>", selecionar)


# 9. INICIAR SISTEMA

conectar()
listar()

janela.mainloop()