import tkinter as tk
from tkinter import ttk, messagebox

from repositories.disciplina_repository import (
    cadastrar_disciplina,
    listar_disciplinas
)


class DisciplinasView:

    def __init__(self, parent):

        self.janela = tk.Toplevel(parent)

        self.janela.title("Cadastro de Disciplinas")
        self.janela.geometry("900x600")

        self.criar_interface()
        self.carregar_disciplinas()

    # ==================================================
    # INTERFACE
    # ==================================================

    def criar_interface(self):

        frame_form = ttk.LabelFrame(
            self.janela,
            text="Dados da disciplina"
        )

        frame_form.pack(
            fill="x",
            padx=10,
            pady=10
        )

        # NOME

        ttk.Label(
            frame_form,
            text="Nome:"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

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

        # CÓDIGO

        ttk.Label(
            frame_form,
            text="Código:"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.entry_codigo = ttk.Entry(
            frame_form,
            width=40
        )

        self.entry_codigo.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        # CARGA HORÁRIA

        ttk.Label(
            frame_form,
            text="Carga horária (horas):"
        ).grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.entry_carga = ttk.Entry(
            frame_form,
            width=15
        )

        self.entry_carga.grid(
            row=2,
            column=1,
            padx=5,
            pady=5,
            sticky="w"
        )

        # MINUTOS POR HORA-AULA

        ttk.Label(
            frame_form,
            text="Minutos por hora-aula:"
        ).grid(
            row=3,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.entry_minutos = ttk.Entry(
            frame_form,
            width=15
        )

        self.entry_minutos.insert(
            0,
            "50"
        )

        self.entry_minutos.grid(
            row=3,
            column=1,
            padx=5,
            pady=5,
            sticky="w"
        )

        # ==================================================
        # BOTÕES
        # ==================================================

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
            text="Nova",
            command=self.nova_disciplina
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            frame_botoes,
            text="Salvar",
            command=self.salvar_disciplina
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            frame_botoes,
            text="Atualizar lista",
            command=self.carregar_disciplinas
        ).pack(
            side="left",
            padx=5
        )

        # ==================================================
        # TABELA
        # ==================================================

        frame_tabela = ttk.LabelFrame(
            self.janela,
            text="Disciplinas cadastradas"
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
            "codigo",
            "carga",
            "minutos"
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
            text="Disciplina"
        )

        self.tabela.heading(
            "codigo",
            text="Código"
        )

        self.tabela.heading(
            "carga",
            text="Carga horária"
        )

        self.tabela.heading(
            "minutos",
            text="Min./hora-aula"
        )

        self.tabela.column(
            "id",
            width=50
        )

        self.tabela.column(
            "nome",
            width=300
        )

        self.tabela.column(
            "codigo",
            width=120
        )

        self.tabela.column(
            "carga",
            width=120
        )

        self.tabela.column(
            "minutos",
            width=120
        )

        self.tabela.pack(
            fill="both",
            expand=True
        )

    # ==================================================
    # CARREGAR
    # ==================================================

    def carregar_disciplinas(self):

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        disciplinas = listar_disciplinas()

        for disciplina in disciplinas:

            self.tabela.insert(
                "",
                "end",
                values=(
                    disciplina["id"],
                    disciplina["nome"],
                    disciplina["codigo"],
                    disciplina["carga_horaria"],
                    disciplina["minutos_hora_aula"]
                )
            )

    # ==================================================
    # NOVA
    # ==================================================

    def nova_disciplina(self):

        self.entry_nome.delete(
            0,
            tk.END
        )

        self.entry_codigo.delete(
            0,
            tk.END
        )

        self.entry_carga.delete(
            0,
            tk.END
        )

        self.entry_minutos.delete(
            0,
            tk.END
        )

        self.entry_minutos.insert(
            0,
            "50"
        )

        self.entry_nome.focus()

    # ==================================================
    # SALVAR
    # ==================================================

    def salvar_disciplina(self):

        nome = self.entry_nome.get().strip()
        codigo = self.entry_codigo.get().strip()
        carga = self.entry_carga.get().strip()
        minutos = self.entry_minutos.get().strip()

        if not nome:

            messagebox.showwarning(
                "Validação",
                "Informe o nome da disciplina."
            )

            return

        if not carga:

            messagebox.showwarning(
                "Validação",
                "Informe a carga horária."
            )

            return

        try:

            carga = float(carga)

        except ValueError:

            messagebox.showwarning(
                "Validação",
                "A carga horária deve ser um número."
            )

            return

        try:

            minutos = int(minutos)

        except ValueError:

            messagebox.showwarning(
                "Validação",
                "Os minutos por hora-aula devem ser um número inteiro."
            )

            return

        if carga <= 0:

            messagebox.showwarning(
                "Validação",
                "A carga horária deve ser maior que zero."
            )

            return

        if minutos <= 0:

            messagebox.showwarning(
                "Validação",
                "Os minutos por hora-aula devem ser maiores que zero."
            )

            return

        try:

            cadastrar_disciplina(
                nome,
                codigo if codigo else None,
                carga,
                minutos
            )

            messagebox.showinfo(
                "Sucesso",
                "Disciplina cadastrada com sucesso."
            )

            self.nova_disciplina()
            self.carregar_disciplinas()

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível cadastrar a disciplina.\n\n{erro}"
            )