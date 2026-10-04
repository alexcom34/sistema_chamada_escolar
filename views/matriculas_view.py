import tkinter as tk
from tkinter import ttk, messagebox

from repositories.turma_repository import listar_turmas
from repositories.aluno_repository import listar_alunos
from repositories.matricula_repository import (
    matricular_aluno,
    listar_alunos_da_turma,
    remover_aluno_da_turma
)


class MatriculasView:

    def __init__(self, parent):

        self.janela = tk.Toplevel(parent)

        self.janela.title("Matrícula de Alunos")

        self.janela.geometry("900x600")

        self.turmas = []
        self.alunos = []

        self.turma_selecionada = None

        self.criar_interface()

        self.carregar_turmas()
        self.carregar_alunos()

    # ==================================================
    # INTERFACE
    # ==================================================

    def criar_interface(self):

        # ==============================================
        # SELEÇÃO DA TURMA
        # ==============================================

        frame_turma = ttk.LabelFrame(
            self.janela,
            text="Turma"
        )

        frame_turma.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(
            frame_turma,
            text="Selecione a turma:"
        ).pack(
            side="left",
            padx=5,
            pady=10
        )

        self.combo_turma = ttk.Combobox(
            frame_turma,
            state="readonly",
            width=50
        )

        self.combo_turma.pack(
            side="left",
            padx=5
        )

        self.combo_turma.bind(
            "<<ComboboxSelected>>",
            self.selecionar_turma
        )

        # ==============================================
        # ALUNO PARA MATRICULAR
        # ==============================================

        frame_aluno = ttk.LabelFrame(
            self.janela,
            text="Matricular aluno"
        )

        frame_aluno.pack(
            fill="x",
            padx=10,
            pady=5
        )

        ttk.Label(
            frame_aluno,
            text="Aluno:"
        ).pack(
            side="left",
            padx=5,
            pady=10
        )

        self.combo_aluno = ttk.Combobox(
            frame_aluno,
            state="readonly",
            width=50
        )

        self.combo_aluno.pack(
            side="left",
            padx=5
        )

        ttk.Button(
            frame_aluno,
            text="Matricular",
            command=self.matricular
        ).pack(
            side="left",
            padx=10
        )

        # ==============================================
        # ALUNOS DA TURMA
        # ==============================================

        frame_lista = ttk.LabelFrame(
            self.janela,
            text="Alunos matriculados"
        )

        frame_lista.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        colunas = (
            "id",
            "nome",
            "matricula",
            "data"
        )

        self.tabela = ttk.Treeview(
            frame_lista,
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
            "data",
            text="Data da matrícula"
        )

        self.tabela.column(
            "id",
            width=60
        )

        self.tabela.column(
            "nome",
            width=300
        )

        self.tabela.column(
            "matricula",
            width=150
        )

        self.tabela.column(
            "data",
            width=150
        )

        self.tabela.pack(
            fill="both",
            expand=True
        )

        # ==============================================
        # BOTÃO REMOVER
        # ==============================================

        ttk.Button(
            self.janela,
            text="Remover aluno da turma",
            command=self.remover
        ).pack(
            pady=10
        )

    # ==================================================
    # CARREGAR TURMAS
    # ==================================================

    def carregar_turmas(self):

        self.turmas = listar_turmas()

        valores = []

        for turma in self.turmas:

            texto = (
                f'{turma["id"]} - '
                f'{turma["nome"]} '
                f'({turma["ano"]}/{turma["semestre"]})'
            )

            valores.append(texto)

        self.combo_turma["values"] = valores

    # ==================================================
    # CARREGAR ALUNOS
    # ==================================================

    def carregar_alunos(self):

        self.alunos = listar_alunos()

        valores = []

        for aluno in self.alunos:

            texto = (
                f'{aluno["id"]} - '
                f'{aluno["nome"]} '
                f'({aluno["matricula"]})'
            )

            valores.append(texto)

        self.combo_aluno["values"] = valores

    # ==================================================
    # SELECIONAR TURMA
    # ==================================================

    def selecionar_turma(self, evento):

        indice = self.combo_turma.current()

        if indice < 0:
            return

        self.turma_selecionada = self.turmas[indice]["id"]

        self.carregar_matriculados()

    # ==================================================
    # CARREGAR MATRICULADOS
    # ==================================================

    def carregar_matriculados(self):

        for item in self.tabela.get_children():

            self.tabela.delete(item)

        if self.turma_selecionada is None:
            return

        alunos = listar_alunos_da_turma(
            self.turma_selecionada
        )

        for aluno in alunos:

            data = aluno["data_matricula"]

            if data:
                data = data.strftime("%d/%m/%Y")

            self.tabela.insert(
                "",
                "end",
                values=(
                    aluno["id"],
                    aluno["nome"],
                    aluno["matricula"],
                    data
                )
            )

    # ==================================================
    # MATRICULAR
    # ==================================================

    def matricular(self):

        if self.turma_selecionada is None:

            messagebox.showwarning(
                "Atenção",
                "Selecione uma turma."
            )

            return

        indice = self.combo_aluno.current()

        if indice < 0:

            messagebox.showwarning(
                "Atenção",
                "Selecione um aluno."
            )

            return

        aluno_id = self.alunos[indice]["id"]

        try:

            matricular_aluno(
                aluno_id,
                self.turma_selecionada
            )

            messagebox.showinfo(
                "Sucesso",
                "Aluno matriculado com sucesso."
            )

            self.combo_aluno.set("")

            self.carregar_matriculados()

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível matricular o aluno.\n\n{erro}"
            )

    # ==================================================
    # REMOVER
    # ==================================================

    def remover(self):

        if self.turma_selecionada is None:

            messagebox.showwarning(
                "Atenção",
                "Selecione uma turma."
            )

            return

        selecionado = self.tabela.selection()

        if not selecionado:

            messagebox.showwarning(
                "Atenção",
                "Selecione um aluno matriculado."
            )

            return

        item = self.tabela.item(
            selecionado[0]
        )

        aluno_id = item["values"][0]

        confirmar = messagebox.askyesno(
            "Confirmar",
            "Deseja remover este aluno da turma?"
        )

        if not confirmar:
            return

        try:

            remover_aluno_da_turma(
                aluno_id,
                self.turma_selecionada
            )

            messagebox.showinfo(
                "Sucesso",
                "Aluno removido da turma."
            )

            self.carregar_matriculados()

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível remover o aluno.\n\n{erro}"
            )