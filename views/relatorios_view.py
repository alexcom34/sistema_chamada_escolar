import tkinter as tk
from tkinter import ttk, messagebox

from repositories.turma_repository import listar_turmas
from repositories.turma_disciplina_repository import (
    listar_disciplinas_da_turma
)
from repositories.relatorio_repository import (
    relatorio_frequencia_turma_disciplina
)


class RelatoriosView:

    def __init__(self, master):

        self.janela = tk.Toplevel(master)

        self.janela.title(
            "Relatórios de Frequência"
        )

        self.janela.geometry(
            "1000x600"
        )

        self.opcoes = []

        self.criar_interface()

        self.carregar_turmas()

    # ==========================================================
    # INTERFACE
    # ==========================================================

    def criar_interface(self):

        frame_filtros = ttk.LabelFrame(
            self.janela,
            text="Filtros"
        )

        frame_filtros.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(
            frame_filtros,
            text="Turma / Disciplina:"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.combo_disciplina = ttk.Combobox(
            frame_filtros,
            width=60,
            state="readonly"
        )

        self.combo_disciplina.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        ttk.Button(
            frame_filtros,
            text="Gerar Relatório",
            command=self.gerar_relatorio
        ).grid(
            row=0,
            column=2,
            padx=10,
            pady=10
        )

        # ======================================================
        # TABELA
        # ======================================================

        frame_tabela = ttk.LabelFrame(
            self.janela,
            text="Frequência dos Alunos"
        )

        frame_tabela.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        colunas = (
            "aluno",
            "matricula",
            "total",
            "presencas",
            "faltas",
            "justificadas",
            "frequencia"
        )

        self.tree = ttk.Treeview(
            frame_tabela,
            columns=colunas,
            show="headings"
        )

        self.tree.heading(
            "aluno",
            text="Aluno"
        )

        self.tree.heading(
            "matricula",
            text="Matrícula"
        )

        self.tree.heading(
            "total",
            text="Total"
        )

        self.tree.heading(
            "presencas",
            text="Presenças"
        )

        self.tree.heading(
            "faltas",
            text="Faltas"
        )

        self.tree.heading(
            "justificadas",
            text="Justificadas"
        )

        self.tree.heading(
            "frequencia",
            text="Frequência"
        )

        self.tree.column(
            "aluno",
            width=250
        )

        self.tree.column(
            "matricula",
            width=130
        )

        self.tree.column(
            "total",
            width=80,
            anchor="center"
        )

        self.tree.column(
            "presencas",
            width=100,
            anchor="center"
        )

        self.tree.column(
            "faltas",
            width=80,
            anchor="center"
        )

        self.tree.column(
            "justificadas",
            width=110,
            anchor="center"
        )

        self.tree.column(
            "frequencia",
            width=110,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            frame_tabela,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

    # ==========================================================
    # CARREGAR TURMAS
    # ==========================================================

    def carregar_turmas(self):

        self.opcoes.clear()

        valores = []

        turmas = listar_turmas()

        for turma in turmas:

            disciplinas = listar_disciplinas_da_turma(
                turma["id"]
            )

            for disciplina in disciplinas:

                texto = (
                    f'{turma["nome"]} | '
                    f'{disciplina["disciplina"]}'
                )

                valores.append(texto)

                self.opcoes.append({
                    "turma_disciplina_id": disciplina["id"],
                    "turma_id": turma["id"],
                    "turma": turma["nome"],
                    "disciplina": disciplina["disciplina"]
                })

        self.combo_disciplina["values"] = valores

        if valores:
            self.combo_disciplina.current(0)

    # ==========================================================
    # GERAR
    # ==========================================================

    def gerar_relatorio(self):

        indice = self.combo_disciplina.current()

        if indice < 0:

            messagebox.showwarning(
                "Aviso",
                "Selecione uma turma e disciplina."
            )

            return

        opcao = self.opcoes[indice]

        resultado = relatorio_frequencia_turma_disciplina(
            opcao["turma_disciplina_id"]
        )

        for item in self.tree.get_children():

            self.tree.delete(item)

        if not resultado:

            messagebox.showinfo(
                "Resultado",
                "Não existem alunos matriculados."
            )

            return

        for aluno in resultado:

            total = int(
                aluno["total_horas"] or 0
            )

            presencas = int(
                aluno["presencas"] or 0
            )

            faltas = int(
                aluno["faltas"] or 0
            )

            justificadas = int(
                aluno["justificadas"] or 0
            )

            total_considerado = (
                presencas +
                faltas +
                justificadas
            )

            if total_considerado > 0:

                frequencia = (
                    presencas /
                    total_considerado
                ) * 100

            else:

                frequencia = 0

            self.tree.insert(
                "",
                "end",
                values=(
                    aluno["aluno"],
                    aluno["matricula"],
                    total,
                    presencas,
                    faltas,
                    justificadas,
                    f"{frequencia:.2f}%"
                )
            )