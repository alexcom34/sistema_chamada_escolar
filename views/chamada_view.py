import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date

from repositories.turma_repository import listar_turmas
from repositories.turma_disciplina_repository import listar_disciplinas_da_turma
from repositories.matricula_repository import listar_alunos_da_turma
from services.chamada_service import registrar_chamada


class ChamadaView:

    def __init__(self, master):
        self.janela = tk.Toplevel(master)
        self.janela.title("Registro de Chamada")
        self.janela.geometry("1100x700")
        self.janela.resizable(True, True)

        self.opcoes_disciplinas = []
        self.alunos = []
        self.status_widgets = {}

        self.criar_interface()
        self.carregar_turmas_disciplinas()

    def criar_interface(self):

        # =========================
        # CABEÇALHO
        # =========================

        frame_topo = ttk.LabelFrame(
            self.janela,
            text="Dados da Aula"
        )
        frame_topo.pack(
            fill="x",
            padx=10,
            pady=10
        )

        # Turma / Disciplina
        ttk.Label(
            frame_topo,
            text="Turma / Disciplina:"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.combo_disciplina = ttk.Combobox(
            frame_topo,
            width=60,
            state="readonly"
        )
        self.combo_disciplina.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky="w"
        )

        # Data
        ttk.Label(
            frame_topo,
            text="Data:"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.entry_data = ttk.Entry(
            frame_topo,
            width=15
        )
        self.entry_data.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.entry_data.insert(
            0,
            date.today().strftime("%d/%m/%Y")
        )

        # Quantidade de horas
        ttk.Label(
            frame_topo,
            text="Horas-aula:"
        ).grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.combo_horas = ttk.Combobox(
            frame_topo,
            width=10,
            state="readonly",
            values=["1", "2", "3", "4", "5", "6", "7", "8"]
        )
        self.combo_horas.grid(
            row=2,
            column=1,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.combo_horas.set("1")

        # Observação
        ttk.Label(
            frame_topo,
            text="Observação:"
        ).grid(
            row=3,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.entry_observacao = ttk.Entry(
            frame_topo,
            width=65
        )
        self.entry_observacao.grid(
            row=3,
            column=1,
            padx=5,
            pady=5,
            sticky="w"
        )

        # Botão montar chamada
        ttk.Button(
            frame_topo,
            text="Montar Chamada",
            command=self.montar_chamada
        ).grid(
            row=4,
            column=1,
            padx=5,
            pady=10,
            sticky="w"
        )

        # =========================
        # MATRIZ DA CHAMADA
        # =========================

        self.frame_chamada = ttk.LabelFrame(
            self.janela,
            text="Registro de Presença"
        )
        self.frame_chamada.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        self.canvas = tk.Canvas(
            self.frame_chamada
        )

        self.scrollbar_vertical = ttk.Scrollbar(
            self.frame_chamada,
            orient="vertical",
            command=self.canvas.yview
        )

        self.scrollbar_horizontal = ttk.Scrollbar(
            self.frame_chamada,
            orient="horizontal",
            command=self.canvas.xview
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar_vertical.set,
            xscrollcommand=self.scrollbar_horizontal.set
        )

        self.scrollbar_vertical.pack(
            side="right",
            fill="y"
        )

        self.scrollbar_horizontal.pack(
            side="bottom",
            fill="x"
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.frame_matriz = ttk.Frame(
            self.canvas
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.frame_matriz,
            anchor="nw"
        )

        self.frame_matriz.bind(
            "<Configure>",
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        # =========================
        # BOTÃO REGISTRAR
        # =========================

        frame_botao = ttk.Frame(
            self.janela
        )
        frame_botao.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Button(
            frame_botao,
            text="Registrar Chamada",
            command=self.registrar
        ).pack(
            side="right"
        )

    # ==========================================================
    # CARREGAR TURMAS E DISCIPLINAS
    # ==========================================================

    def carregar_turmas_disciplinas(self):

        self.opcoes_disciplinas.clear()

        turmas = listar_turmas()

        valores = []

        for turma in turmas:

            disciplinas = listar_disciplinas_da_turma(
                turma["id"]
            )

            for disciplina in disciplinas:

                professor = disciplina["professor"]

                if professor is None:
                    professor = "Sem professor"

                texto = (
                    f'{turma["nome"]} | '
                    f'{disciplina["disciplina"]} | '
                    f'{professor}'
                )

                valores.append(texto)

                self.opcoes_disciplinas.append({
                    "turma_id": turma["id"],
                    "turma_disciplina_id": disciplina["id"],
                    "turma_nome": turma["nome"],
                    "disciplina": disciplina["disciplina"]
                })

        self.combo_disciplina["values"] = valores

        if valores:
            self.combo_disciplina.current(0)

    # ==========================================================
    # CONVERTER DATA
    # ==========================================================

    def converter_data(self):

        texto = self.entry_data.get().strip()

        try:
            return datetime.strptime(
                texto,
                "%d/%m/%Y"
            ).date()

        except ValueError:
            raise ValueError(
                "Data inválida.\n\n"
                "Use o formato DD/MM/AAAA."
            )

    # ==========================================================
    # MONTAR CHAMADA
    # ==========================================================

    def montar_chamada(self):

        if not self.opcoes_disciplinas:
            messagebox.showwarning(
                "Aviso",
                "Não existem disciplinas vinculadas às turmas."
            )
            return

        indice = self.combo_disciplina.current()

        if indice < 0:
            messagebox.showwarning(
                "Aviso",
                "Selecione uma turma/disciplina."
            )
            return

        try:
            quantidade_horas = int(
                self.combo_horas.get()
            )

        except ValueError:
            messagebox.showerror(
                "Erro",
                "Quantidade de horas-aula inválida."
            )
            return

        opcao = self.opcoes_disciplinas[indice]

        turma_id = opcao["turma_id"]

        alunos = listar_alunos_da_turma(
            turma_id
        )

        if not alunos:
            messagebox.showwarning(
                "Aviso",
                "Essa turma não possui alunos matriculados."
            )
            return

        self.alunos = alunos

        self.criar_matriz(
            quantidade_horas
        )

    # ==========================================================
    # CRIAR MATRIZ
    # ==========================================================

    def criar_matriz(self, quantidade_horas):

        # Limpa matriz anterior
        for widget in self.frame_matriz.winfo_children():
            widget.destroy()

        self.status_widgets.clear()

        # =========================
        # CABEÇALHO
        # =========================

        ttk.Label(
            self.frame_matriz,
            text="Aluno",
            font=("Arial", 10, "bold")
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=8,
            sticky="w"
        )

        ttk.Label(
            self.frame_matriz,
            text="Matrícula",
            font=("Arial", 10, "bold")
        ).grid(
            row=0,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )

        for hora in range(
            1,
            quantidade_horas + 1
        ):

            ttk.Label(
                self.frame_matriz,
                text=f"{hora}ª Hora",
                font=("Arial", 10, "bold")
            ).grid(
                row=0,
                column=hora + 1,
                padx=10,
                pady=8
            )

        # =========================
        # ALUNOS
        # =========================

        status = [
            "PRESENTE",
            "FALTA",
            "JUSTIFICADA"
        ]

        for linha, aluno in enumerate(
            self.alunos,
            start=1
        ):

            ttk.Label(
                self.frame_matriz,
                text=aluno["nome"]
            ).grid(
                row=linha,
                column=0,
                padx=10,
                pady=5,
                sticky="w"
            )

            ttk.Label(
                self.frame_matriz,
                text=aluno["matricula"]
            ).grid(
                row=linha,
                column=1,
                padx=10,
                pady=5,
                sticky="w"
            )

            for hora in range(
                1,
                quantidade_horas + 1
            ):

                combo = ttk.Combobox(
                    self.frame_matriz,
                    width=14,
                    values=status,
                    state="readonly"
                )

                combo.set("PRESENTE")

                combo.grid(
                    row=linha,
                    column=hora + 1,
                    padx=5,
                    pady=5
                )

                self.status_widgets[
                    (aluno["id"], hora)
                ] = combo

        self.canvas.update_idletasks()

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    # ==========================================================
    # REGISTRAR CHAMADA
    # ==========================================================

    def registrar(self):

        if not self.alunos:
            messagebox.showwarning(
                "Aviso",
                "Monte a chamada antes de registrar."
            )
            return

        indice = self.combo_disciplina.current()

        if indice < 0:
            messagebox.showwarning(
                "Aviso",
                "Selecione uma turma/disciplina."
            )
            return

        try:

            data_aula = self.converter_data()

            quantidade_horas = int(
                self.combo_horas.get()
            )

        except ValueError as erro:

            messagebox.showerror(
                "Erro",
                str(erro)
            )
            return

        opcao = self.opcoes_disciplinas[indice]

        presencas = []

        for aluno in self.alunos:

            for hora in range(
                1,
                quantidade_horas + 1
            ):

                widget = self.status_widgets.get(
                    (aluno["id"], hora)
                )

                if widget is None:
                    messagebox.showerror(
                        "Erro",
                        "A matriz da chamada está incompleta."
                    )
                    return

                status = widget.get()

                if status not in [
                    "PRESENTE",
                    "FALTA",
                    "JUSTIFICADA"
                ]:
                    messagebox.showerror(
                        "Erro",
                        "Existe uma situação de presença inválida."
                    )
                    return

                presencas.append({
                    "aluno_id": aluno["id"],
                    "hora": hora,
                    "status": status
                })

        observacao = (
            self.entry_observacao.get().strip()
            or None
        )

        try:

            registrar_chamada(
                turma_disciplina_id=opcao[
                    "turma_disciplina_id"
                ],
                data_aula=data_aula,
                quantidade_horas_aula=quantidade_horas,
                presencas=presencas,
                observacao=observacao
            )

            messagebox.showinfo(
                "Sucesso",
                "Chamada registrada com sucesso."
            )

            self.limpar_tela()

        except Exception as erro:

            messagebox.showerror(
                "Erro ao registrar chamada",
                str(erro)
            )

    # ==========================================================
    # LIMPAR
    # ==========================================================

    def limpar_tela(self):

        self.alunos = []
        self.status_widgets.clear()

        for widget in self.frame_matriz.winfo_children():
            widget.destroy()

        self.entry_observacao.delete(
            0,
            tk.END
        )