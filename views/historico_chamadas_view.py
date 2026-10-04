import tkinter as tk
from tkinter import ttk, messagebox

from repositories.aula_repository import (
    listar_aulas,
    buscar_aula_por_id
)

from repositories.presenca_repository import (
    listar_presencas_da_aula
)


class HistoricoChamadasView:

    def __init__(self, master):

        self.janela = tk.Toplevel(master)

        self.janela.title(
            "Histórico de Chamadas"
        )

        self.janela.geometry(
            "1100x650"
        )

        self.criar_interface()

        self.carregar_aulas()

    # ==========================================================
    # INTERFACE
    # ==========================================================

    def criar_interface(self):

        frame_lista = ttk.LabelFrame(
            self.janela,
            text="Aulas Registradas"
        )

        frame_lista.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        colunas = (
            "id",
            "data",
            "turma",
            "disciplina",
            "professor",
            "horas",
            "observacao"
        )

        self.tree_aulas = ttk.Treeview(
            frame_lista,
            columns=colunas,
            show="headings"
        )

        self.tree_aulas.heading(
            "id",
            text="ID"
        )

        self.tree_aulas.heading(
            "data",
            text="Data"
        )

        self.tree_aulas.heading(
            "turma",
            text="Turma"
        )

        self.tree_aulas.heading(
            "disciplina",
            text="Disciplina"
        )

        self.tree_aulas.heading(
            "professor",
            text="Professor"
        )

        self.tree_aulas.heading(
            "horas",
            text="Horas"
        )

        self.tree_aulas.heading(
            "observacao",
            text="Observação"
        )

        self.tree_aulas.column(
            "id",
            width=50
        )

        self.tree_aulas.column(
            "data",
            width=100
        )

        self.tree_aulas.column(
            "turma",
            width=180
        )

        self.tree_aulas.column(
            "disciplina",
            width=220
        )

        self.tree_aulas.column(
            "professor",
            width=180
        )

        self.tree_aulas.column(
            "horas",
            width=70
        )

        self.tree_aulas.column(
            "observacao",
            width=220
        )

        scrollbar = ttk.Scrollbar(
            frame_lista,
            orient="vertical",
            command=self.tree_aulas.yview
        )

        self.tree_aulas.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree_aulas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.tree_aulas.bind(
            "<Double-1>",
            self.abrir_detalhes
        )

        # ======================================================
        # BOTÕES
        # ======================================================

        frame_botoes = ttk.Frame(
            self.janela
        )

        frame_botoes.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Button(
            frame_botoes,
            text="Atualizar",
            command=self.carregar_aulas
        ).pack(
            side="left"
        )

        ttk.Button(
            frame_botoes,
            text="Ver Chamada",
            command=self.abrir_detalhes
        ).pack(
            side="left",
            padx=10
        )

    # ==========================================================
    # CARREGAR AULAS
    # ==========================================================

    def carregar_aulas(self):

        for item in self.tree_aulas.get_children():

            self.tree_aulas.delete(
                item
            )

        aulas = listar_aulas()

        for aula in aulas:

            data = aula["data_aula"]

            if hasattr(data, "strftime"):
                data = data.strftime(
                    "%d/%m/%Y"
                )

            professor = (
                aula["professor"]
                if aula["professor"]
                else "Não informado"
            )

            observacao = (
                aula["observacao"]
                if aula["observacao"]
                else ""
            )

            self.tree_aulas.insert(
                "",
                "end",
                values=(
                    aula["id"],
                    data,
                    aula["turma"],
                    aula["disciplina"],
                    professor,
                    aula["quantidade_horas_aula"],
                    observacao
                )
            )

    # ==========================================================
    # ABRIR DETALHES
    # ==========================================================

    def abrir_detalhes(self, event=None):

        selecionado = (
            self.tree_aulas.selection()
        )

        if not selecionado:

            messagebox.showwarning(
                "Aviso",
                "Selecione uma aula."
            )

            return

        item = self.tree_aulas.item(
            selecionado[0]
        )

        aula_id = item["values"][0]

        aula = buscar_aula_por_id(
            aula_id
        )

        presencas = listar_presencas_da_aula(
            aula_id
        )

        if aula is None:

            messagebox.showerror(
                "Erro",
                "A aula não foi encontrada."
            )

            return

        self.mostrar_detalhes(
            aula,
            presencas
        )

    # ==========================================================
    # DETALHES
    # ==========================================================

    def mostrar_detalhes(
        self,
        aula,
        presencas
    ):

        janela = tk.Toplevel(
            self.janela
        )

        janela.title(
            "Detalhes da Chamada"
        )

        janela.geometry(
            "850x550"
        )

        frame_info = ttk.LabelFrame(
            janela,
            text="Informações da Aula"
        )

        frame_info.pack(
            fill="x",
            padx=10,
            pady=10
        )

        data = aula["data_aula"]

        if hasattr(data, "strftime"):
            data = data.strftime(
                "%d/%m/%Y"
            )

        ttk.Label(
            frame_info,
            text=f"Turma: {aula['turma']}"
        ).pack(
            anchor="w",
            padx=10,
            pady=3
        )

        ttk.Label(
            frame_info,
            text=f"Disciplina: {aula['disciplina']}"
        ).pack(
            anchor="w",
            padx=10,
            pady=3
        )

        ttk.Label(
            frame_info,
            text=f"Professor: {aula['professor'] or 'Não informado'}"
        ).pack(
            anchor="w",
            padx=10,
            pady=3
        )

        ttk.Label(
            frame_info,
            text=f"Data: {data}"
        ).pack(
            anchor="w",
            padx=10,
            pady=3
        )

        ttk.Label(
            frame_info,
            text=f"Horas-aula: {aula['quantidade_horas_aula']}"
        ).pack(
            anchor="w",
            padx=10,
            pady=3
        )

        # ======================================================
        # TABELA
        # ======================================================

        frame_tabela = ttk.LabelFrame(
            janela,
            text="Presenças"
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
            "hora",
            "status"
        )

        tree = ttk.Treeview(
            frame_tabela,
            columns=colunas,
            show="headings"
        )

        tree.heading(
            "aluno",
            text="Aluno"
        )

        tree.heading(
            "matricula",
            text="Matrícula"
        )

        tree.heading(
            "hora",
            text="Hora-aula"
        )

        tree.heading(
            "status",
            text="Status"
        )

        tree.column(
            "aluno",
            width=300
        )

        tree.column(
            "matricula",
            width=150
        )

        tree.column(
            "hora",
            width=120
        )

        tree.column(
            "status",
            width=180
        )

        scrollbar = ttk.Scrollbar(
            frame_tabela,
            orient="vertical",
            command=tree.yview
        )

        tree.configure(
            yscrollcommand=scrollbar.set
        )

        tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        for presenca in presencas:

            tree.insert(
                "",
                "end",
                values=(
                    presenca["aluno"],
                    presenca["matricula"],
                    f'{presenca["numero_hora_aula"]}ª',
                    presenca["status"]
                )
            )