import tkinter as tk
from tkinter import ttk, messagebox

from repositories.aluno_repository import (
    cadastrar_aluno,
    listar_alunos,
    atualizar_aluno,
    excluir_aluno
)


class AlunosView:

    def __init__(self, parent):

        self.janela = tk.Toplevel(parent)
        self.janela.title("Cadastro de Alunos")
        self.janela.geometry("800x550")

        self.aluno_selecionado = None

        self.criar_interface()
        self.carregar_alunos()

    def criar_interface(self):

        # =========================
        # FORMULÁRIO
        # =========================

        frame_form = ttk.LabelFrame(
            self.janela,
            text="Dados do aluno"
        )

        frame_form.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(
            frame_form,
            text="Nome:"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.entry_nome = ttk.Entry(
            frame_form,
            width=40
        )

        self.entry_nome.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Label(
            frame_form,
            text="Matrícula:"
        ).grid(row=1, column=0, padx=5, pady=5)

        self.entry_matricula = ttk.Entry(
            frame_form,
            width=40
        )

        self.entry_matricula.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Label(
            frame_form,
            text="E-mail:"
        ).grid(row=2, column=0, padx=5, pady=5)

        self.entry_email = ttk.Entry(
            frame_form,
            width=40
        )

        self.entry_email.grid(
            row=2,
            column=1,
            padx=5,
            pady=5
        )

        # =========================
        # BOTÕES
        # =========================

        frame_botoes = ttk.Frame(
            self.janela
        )

        frame_botoes.pack(
            fill="x",
            padx=10,
            pady=5
        )

        ttk.Button(
            frame_botoes,
            text="Novo",
            command=self.novo_aluno
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            frame_botoes,
            text="Salvar",
            command=self.salvar_aluno
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            frame_botoes,
            text="Inativar",
            command=self.inativar_aluno
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            frame_botoes,
            text="Atualizar lista",
            command=self.carregar_alunos
        ).pack(
            side="left",
            padx=5
        )

        # =========================
        # TABELA
        # =========================

        frame_tabela = ttk.LabelFrame(
            self.janela,
            text="Alunos cadastrados"
        )

        frame_tabela.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        colunas = (
            "id",
            "nome",
            "matricula",
            "email"
        )

        self.tabela = ttk.Treeview(
            frame_tabela,
            columns=colunas,
            show="headings"
        )

        self.tabela.heading(
            "id",
            text="ID"
        )

        self.tabela.heading(
            "nome",
            text="Nome"
        )

        self.tabela.heading(
            "matricula",
            text="Matrícula"
        )

        self.tabela.heading(
            "email",
            text="E-mail"
        )

        self.tabela.column(
            "id",
            width=50
        )

        self.tabela.column(
            "nome",
            width=250
        )

        self.tabela.column(
            "matricula",
            width=120
        )

        self.tabela.column(
            "email",
            width=250
        )

        self.tabela.pack(
            fill="both",
            expand=True
        )

        self.tabela.bind(
            "<<TreeviewSelect>>",
            self.selecionar_aluno
        )

    # =========================
    # CARREGAR ALUNOS
    # =========================

    def carregar_alunos(self):

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        alunos = listar_alunos()

        for aluno in alunos:

            self.tabela.insert(
                "",
                "end",
                values=(
                    aluno["id"],
                    aluno["nome"],
                    aluno["matricula"],
                    aluno["email"] or ""
                )
            )

    # =========================
    # SELECIONAR ALUNO
    # =========================

    def selecionar_aluno(self, evento):

        selecionado = self.tabela.selection()

        if not selecionado:
            return

        item = self.tabela.item(
            selecionado[0]
        )

        valores = item["values"]

        self.aluno_selecionado = valores[0]

        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, valores[1])

        self.entry_matricula.delete(0, tk.END)
        self.entry_matricula.insert(0, valores[2])

        self.entry_email.delete(0, tk.END)
        self.entry_email.insert(0, valores[3])

    # =========================
    # NOVO ALUNO
    # =========================

    def novo_aluno(self):

        self.aluno_selecionado = None

        self.entry_nome.delete(0, tk.END)
        self.entry_matricula.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)

        self.entry_nome.focus()

    # =========================
    # SALVAR
    # =========================

    def salvar_aluno(self):

        nome = self.entry_nome.get().strip()
        matricula = self.entry_matricula.get().strip()
        email = self.entry_email.get().strip()

        if not nome:
            messagebox.showwarning(
                "Validação",
                "Informe o nome do aluno."
            )
            return

        if not matricula:
            messagebox.showwarning(
                "Validação",
                "Informe a matrícula."
            )
            return

        try:

            if self.aluno_selecionado is None:

                cadastrar_aluno(
                    nome,
                    matricula,
                    email if email else None
                )

                messagebox.showinfo(
                    "Sucesso",
                    "Aluno cadastrado com sucesso."
                )

            else:

                atualizar_aluno(
                    self.aluno_selecionado,
                    nome,
                    matricula,
                    email if email else None
                )

                messagebox.showinfo(
                    "Sucesso",
                    "Aluno atualizado com sucesso."
                )

            self.novo_aluno()
            self.carregar_alunos()

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível salvar o aluno.\n\n{erro}"
            )

    # =========================
    # INATIVAR
    # =========================

    def inativar_aluno(self):

        if self.aluno_selecionado is None:

            messagebox.showwarning(
                "Atenção",
                "Selecione um aluno."
            )

            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "Deseja realmente inativar este aluno?"
        )

        if not confirmar:
            return

        try:

            excluir_aluno(
                self.aluno_selecionado
            )

            messagebox.showinfo(
                "Sucesso",
                "Aluno inativado com sucesso."
            )

            self.novo_aluno()
            self.carregar_alunos()

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível inativar o aluno.\n\n{erro}"
            )