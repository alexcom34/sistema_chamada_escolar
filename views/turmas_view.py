import tkinter as tk
from tkinter import ttk, messagebox

from repositories.turma_repository import (
    cadastrar_turma,
    listar_turmas,
    atualizar_turma,
    inativar_turma
)

from repositories.professor_repository import (
    listar_professores
)


class TurmasView:

    def __init__(self, parent):

        self.janela = tk.Toplevel(parent)

        self.janela.title("Cadastro de Turmas")
        self.janela.geometry("900x600")

        self.turma_selecionada = None
        self.professores = []

        self.criar_interface()
        self.carregar_professores()
        self.carregar_turmas()

    # ==================================================
    # INTERFACE
    # ==================================================

    def criar_interface(self):

        frame_form = ttk.LabelFrame(
            self.janela,
            text="Dados da turma"
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

        # ANO

        ttk.Label(
            frame_form,
            text="Ano:"
        ).grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.entry_ano = ttk.Entry(
            frame_form,
            width=10
        )

        self.entry_ano.grid(
            row=2,
            column=1,
            padx=5,
            pady=5,
            sticky="w"
        )

        # SEMESTRE

        ttk.Label(
            frame_form,
            text="Semestre:"
        ).grid(
            row=3,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.combo_semestre = ttk.Combobox(
            frame_form,
            values=["1", "2"],
            state="readonly",
            width=8
        )

        self.combo_semestre.grid(
            row=3,
            column=1,
            padx=5,
            pady=5,
            sticky="w"
        )

        # PROFESSOR

        ttk.Label(
            frame_form,
            text="Professor:"
        ).grid(
            row=4,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.combo_professor = ttk.Combobox(
            frame_form,
            state="readonly",
            width=37
        )

        self.combo_professor.grid(
            row=4,
            column=1,
            padx=5,
            pady=5
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
            command=self.nova_turma
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            frame_botoes,
            text="Salvar",
            command=self.salvar_turma
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            frame_botoes,
            text="Inativar",
            command=self.inativar_turma
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            frame_botoes,
            text="Atualizar lista",
            command=self.carregar_turmas
        ).pack(
            side="left",
            padx=5
        )

        # ==================================================
        # TABELA
        # ==================================================

        frame_tabela = ttk.LabelFrame(
            self.janela,
            text="Turmas cadastradas"
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
            "ano",
            "semestre",
            "professor"
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
            "codigo",
            text="Código"
        )

        self.tabela.heading(
            "ano",
            text="Ano"
        )

        self.tabela.heading(
            "semestre",
            text="Semestre"
        )

        self.tabela.heading(
            "professor",
            text="Professor"
        )

        self.tabela.column(
            "id",
            width=50
        )

        self.tabela.column(
            "nome",
            width=220
        )

        self.tabela.column(
            "codigo",
            width=150
        )

        self.tabela.column(
            "ano",
            width=70
        )

        self.tabela.column(
            "semestre",
            width=80
        )

        self.tabela.column(
            "professor",
            width=220
        )

        self.tabela.pack(
            fill="both",
            expand=True
        )

        self.tabela.bind(
            "<<TreeviewSelect>>",
            self.selecionar_turma
        )

    # ==================================================
    # PROFESSORES
    # ==================================================

    def carregar_professores(self):

        self.professores = listar_professores()

        nomes = [
            professor["nome"]
            for professor in self.professores
        ]

        self.combo_professor["values"] = nomes

    # ==================================================
    # TURMAS
    # ==================================================

    def carregar_turmas(self):

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        turmas = listar_turmas()

        professores = {
            professor["id"]: professor["nome"]
            for professor in self.professores
        }

        for turma in turmas:

            professor_nome = professores.get(
                turma["professor_id"],
                ""
            )

            self.tabela.insert(
                "",
                "end",
                values=(
                    turma["id"],
                    turma["nome"],
                    turma["codigo"],
                    turma["ano"],
                    turma["semestre"],
                    professor_nome
                )
            )

    # ==================================================
    # SELECIONAR TURMA
    # ==================================================

    def selecionar_turma(self, evento):

        selecionado = self.tabela.selection()

        if not selecionado:
            return

        item = self.tabela.item(
            selecionado[0]
        )

        valores = item["values"]

        self.turma_selecionada = valores[0]

        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(
            0,
            valores[1]
        )

        self.entry_codigo.delete(0, tk.END)
        self.entry_codigo.insert(
            0,
            valores[2]
        )

        self.entry_ano.delete(0, tk.END)
        self.entry_ano.insert(
            0,
            valores[3]
        )

        self.combo_semestre.set(
            valores[4]
        )

        self.combo_professor.set(
            valores[5]
        )

    # ==================================================
    # NOVA TURMA
    # ==================================================

    def nova_turma(self):

        self.turma_selecionada = None

        self.entry_nome.delete(
            0,
            tk.END
        )

        self.entry_codigo.delete(
            0,
            tk.END
        )

        self.entry_ano.delete(
            0,
            tk.END
        )

        self.combo_semestre.set("")

        self.combo_professor.set("")

        self.entry_nome.focus()

    # ==================================================
    # SALVAR
    # ==================================================

    def salvar_turma(self):

        nome = self.entry_nome.get().strip()
        codigo = self.entry_codigo.get().strip()
        ano = self.entry_ano.get().strip()
        semestre = self.combo_semestre.get()
        professor_nome = self.combo_professor.get()

        if not nome:
            messagebox.showwarning(
                "Validação",
                "Informe o nome da turma."
            )
            return

        if not codigo:
            messagebox.showwarning(
                "Validação",
                "Informe o código da turma."
            )
            return

        if not ano:
            messagebox.showwarning(
                "Validação",
                "Informe o ano."
            )
            return

        if not semestre:
            messagebox.showwarning(
                "Validação",
                "Selecione o semestre."
            )
            return

        try:

            ano = int(ano)

        except ValueError:

            messagebox.showwarning(
                "Validação",
                "O ano deve ser um número."
            )

            return

        professor_id = None

        for professor in self.professores:

            if professor["nome"] == professor_nome:

                professor_id = professor["id"]
                break

        try:

            if self.turma_selecionada is None:

                cadastrar_turma(
                    nome,
                    codigo,
                    ano,
                    int(semestre),
                    professor_id
                )

                messagebox.showinfo(
                    "Sucesso",
                    "Turma cadastrada com sucesso."
                )

            else:

                atualizar_turma(
                    self.turma_selecionada,
                    nome,
                    codigo,
                    ano,
                    int(semestre)
                )

                messagebox.showinfo(
                    "Sucesso",
                    "Turma atualizada com sucesso."
                )

            self.nova_turma()
            self.carregar_turmas()

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível salvar a turma.\n\n{erro}"
            )

    # ==================================================
    # INATIVAR
    # ==================================================

    def inativar_turma(self):

        if self.turma_selecionada is None:

            messagebox.showwarning(
                "Atenção",
                "Selecione uma turma."
            )

            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "Deseja realmente inativar esta turma?"
        )

        if not confirmar:
            return

        try:

            inativar_turma(
                self.turma_selecionada
            )

            messagebox.showinfo(
                "Sucesso",
                "Turma inativada com sucesso."
            )

            self.nova_turma()
            self.carregar_turmas()

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível inativar a turma.\n\n{erro}"
            )