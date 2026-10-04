import tkinter as tk
from tkinter import ttk, messagebox

from repositories.turma_repository import listar_turmas
from repositories.disciplina_repository import listar_disciplinas
from repositories.professor_repository import listar_professores

from repositories.turma_disciplina_repository import (
    vincular_disciplina,
    listar_disciplinas_da_turma,
    disciplina_ja_vinculada
)

from services.carga_horaria_service import calcular_aulas


class TurmaDisciplinasView:

    def __init__(self, parent):

        self.janela = tk.Toplevel(parent)

        self.janela.title("Disciplinas das Turmas")
        self.janela.geometry("1000x650")

        self.turmas = []
        self.disciplinas = []
        self.professores = []

        self.turma_selecionada = None

        self.criar_interface()

        self.carregar_turmas()
        self.carregar_disciplinas()
        self.carregar_professores()

    # ==================================================
    # INTERFACE
    # ==================================================

    def criar_interface(self):

        frame_form = ttk.LabelFrame(
            self.janela,
            text="Vincular disciplina à turma"
        )

        frame_form.pack(
            fill="x",
            padx=10,
            pady=10
        )

        # TURMA

        ttk.Label(
            frame_form,
            text="Turma:"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.combo_turma = ttk.Combobox(
            frame_form,
            state="readonly",
            width=50
        )

        self.combo_turma.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        self.combo_turma.bind(
            "<<ComboboxSelected>>",
            self.selecionar_turma
        )

        # DISCIPLINA

        ttk.Label(
            frame_form,
            text="Disciplina:"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.combo_disciplina = ttk.Combobox(
            frame_form,
            state="readonly",
            width=50
        )

        self.combo_disciplina.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        self.combo_disciplina.bind(
            "<<ComboboxSelected>>",
            self.atualizar_info_disciplina
        )

        # PROFESSOR

        ttk.Label(
            frame_form,
            text="Professor:"
        ).grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.combo_professor = ttk.Combobox(
            frame_form,
            state="readonly",
            width=50
        )

        self.combo_professor.grid(
            row=2,
            column=1,
            padx=5,
            pady=5
        )

        # CARGA HORÁRIA

        ttk.Label(
            frame_form,
            text="Carga horária:"
        ).grid(
            row=3,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.label_carga = ttk.Label(
            frame_form,
            text="-"
        )

        self.label_carga.grid(
            row=3,
            column=1,
            padx=5,
            pady=5,
            sticky="w"
        )

        # MINUTOS

        ttk.Label(
            frame_form,
            text="Minutos por hora-aula:"
        ).grid(
            row=4,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.label_minutos = ttk.Label(
            frame_form,
            text="-"
        )

        self.label_minutos.grid(
            row=4,
            column=1,
            padx=5,
            pady=5,
            sticky="w"
        )

        # TOTAL DE HORAS-AULA

        ttk.Label(
            frame_form,
            text="Total de horas-aula:"
        ).grid(
            row=5,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.label_total_aulas = ttk.Label(
            frame_form,
            text="-"
        )

        self.label_total_aulas.grid(
            row=5,
            column=1,
            padx=5,
            pady=5,
            sticky="w"
        )

        # BOTÃO

        ttk.Button(
            frame_form,
            text="Vincular disciplina",
            command=self.vincular
        ).grid(
            row=6,
            column=1,
            padx=5,
            pady=15,
            sticky="w"
        )

        # ==================================================
        # TABELA
        # ==================================================

        frame_tabela = ttk.LabelFrame(
            self.janela,
            text="Disciplinas vinculadas"
        )

        frame_tabela.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        colunas = (
            "id",
            "disciplina",
            "codigo",
            "carga",
            "minutos",
            "professor",
            "aulas"
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
            "disciplina",
            text="Disciplina"
        )

        self.tabela.heading(
            "codigo",
            text="Código"
        )

        self.tabela.heading(
            "carga",
            text="Carga"
        )

        self.tabela.heading(
            "minutos",
            text="Min./Aula"
        )

        self.tabela.heading(
            "professor",
            text="Professor"
        )

        self.tabela.heading(
            "aulas",
            text="Horas-aula"
        )

        self.tabela.column(
            "id",
            width=50
        )

        self.tabela.column(
            "disciplina",
            width=220
        )

        self.tabela.column(
            "codigo",
            width=100
        )

        self.tabela.column(
            "carga",
            width=80
        )

        self.tabela.column(
            "minutos",
            width=90
        )

        self.tabela.column(
            "professor",
            width=200
        )

        self.tabela.column(
            "aulas",
            width=90
        )

        self.tabela.pack(
            fill="both",
            expand=True
        )

    # ==================================================
    # CARREGAR TURMAS
    # ==================================================

    def carregar_turmas(self):

        self.turmas = listar_turmas()

        valores = []

        for turma in self.turmas:

            valores.append(
                f'{turma["id"]} - '
                f'{turma["nome"]} '
                f'({turma["ano"]}/{turma["semestre"]})'
            )

        self.combo_turma["values"] = valores

    # ==================================================
    # CARREGAR DISCIPLINAS
    # ==================================================

    def carregar_disciplinas(self):

        self.disciplinas = listar_disciplinas()

        valores = []

        for disciplina in self.disciplinas:

            valores.append(
                f'{disciplina["id"]} - '
                f'{disciplina["nome"]}'
            )

        self.combo_disciplina["values"] = valores

    # ==================================================
    # CARREGAR PROFESSORES
    # ==================================================

    def carregar_professores(self):

        self.professores = listar_professores()

        valores = []

        for professor in self.professores:

            valores.append(
                f'{professor["id"]} - '
                f'{professor["nome"]}'
            )

        self.combo_professor["values"] = valores

    # ==================================================
    # SELECIONAR TURMA
    # ==================================================

    def selecionar_turma(self, evento):

        indice = self.combo_turma.current()

        if indice < 0:
            return

        self.turma_selecionada = self.turmas[indice]["id"]

        self.carregar_vinculos()

    # ==================================================
    # DISCIPLINA SELECIONADA
    # ==================================================

    def atualizar_info_disciplina(self, evento):

        indice = self.combo_disciplina.current()

        if indice < 0:
            return

        disciplina = self.disciplinas[indice]

        carga = disciplina["carga_horaria"]
        minutos = disciplina["minutos_hora_aula"]

        total_aulas = calcular_aulas(
            carga,
            minutos
        )

        self.label_carga.config(
            text=f"{carga} horas"
        )

        self.label_minutos.config(
            text=f"{minutos} minutos"
        )

        self.label_total_aulas.config(
            text=f"{total_aulas:g}"
        )

    # ==================================================
    # CARREGAR VÍNCULOS
    # ==================================================

    def carregar_vinculos(self):

        for item in self.tabela.get_children():

            self.tabela.delete(item)

        if self.turma_selecionada is None:
            return

        disciplinas = listar_disciplinas_da_turma(
            self.turma_selecionada
        )

        for disciplina in disciplinas:

            self.tabela.insert(
                "",
                "end",
                values=(
                    disciplina["id"],
                    disciplina["disciplina"],
                    disciplina["codigo"],
                    disciplina["carga_horaria"],
                    disciplina["minutos_hora_aula"],
                    disciplina["professor"] or "",
                    disciplina["aulas_previstas"]
                )
            )

    # ==================================================
    # VINCULAR
    # ==================================================

    def vincular(self):

        if self.turma_selecionada is None:

            messagebox.showwarning(
                "Validação",
                "Selecione uma turma."
            )

            return

        indice_disciplina = self.combo_disciplina.current()

        if indice_disciplina < 0:

            messagebox.showwarning(
                "Validação",
                "Selecione uma disciplina."
            )

            return

        indice_professor = self.combo_professor.current()

        if indice_professor < 0:

            messagebox.showwarning(
                "Validação",
                "Selecione um professor."
            )

            return

        disciplina = self.disciplinas[
            indice_disciplina
        ]

        professor = self.professores[
            indice_professor
        ]
        
        if disciplina_ja_vinculada(
            self.turma_selecionada,
            disciplina["id"]
        ):

            messagebox.showwarning(
                "Disciplina já vinculada",
                "Esta disciplina já está vinculada a esta turma."
            )

            return

        total_aulas = calcular_aulas(
            disciplina["carga_horaria"],
            disciplina["minutos_hora_aula"]
        )

        if total_aulas != int(total_aulas):

            messagebox.showerror(
                "Erro",
                "A carga horária não resulta em um número inteiro de horas-aula."
            )

            return

        try:

            vincular_disciplina(
                self.turma_selecionada,
                disciplina["id"],
                professor["id"],
                int(total_aulas)
            )

            messagebox.showinfo(
                "Sucesso",
                f'Disciplina "{disciplina["nome"]}" vinculada com sucesso.\n\n'
                f"Total de horas-aula: {int(total_aulas)}"
            )

            self.combo_disciplina.set("")
            self.combo_professor.set("")

            self.label_carga.config(
                text="-"
            )

            self.label_minutos.config(
                text="-"
            )

            self.label_total_aulas.config(
                text="-"
            )

            self.carregar_vinculos()

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível realizar o vínculo.\n\n{erro}"
            )