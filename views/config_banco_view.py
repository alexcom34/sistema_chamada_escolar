import tkinter as tk
from tkinter import ttk, messagebox

from config import salvar_config
from database.initializer import (
    testar_conexao,
    criar_banco_e_tabelas
)


class ConfigBancoView:

    def __init__(self, parent):

        self.janela = tk.Toplevel(parent)

        self.janela.title(
            "Configuração do Banco de Dados"
        )

        self.janela.geometry(
            "450x330"
        )

        self.janela.resizable(
            False,
            False
        )

        self.janela.transient(parent)
        self.janela.grab_set()

        self.configurado = False

        self.criar_interface()

    # =========================================================
    # INTERFACE
    # =========================================================

    def criar_interface(self):

        frame = ttk.Frame(
            self.janela,
            padding=20
        )

        frame.pack(
            fill="both",
            expand=True
        )

        titulo = ttk.Label(
            frame,
            text="Configuração do MySQL",
            font=("Arial", 16, "bold")
        )

        titulo.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(0, 20)
        )

        # -----------------------------------------------------
        # HOST
        # -----------------------------------------------------

        ttk.Label(
            frame,
            text="Servidor:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=5
        )

        self.entry_host = ttk.Entry(
            frame,
            width=35
        )

        self.entry_host.grid(
            row=1,
            column=1,
            pady=5
        )

        self.entry_host.insert(
            0,
            "localhost"
        )

        # -----------------------------------------------------
        # PORTA
        # -----------------------------------------------------

        ttk.Label(
            frame,
            text="Porta:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=5
        )

        self.entry_port = ttk.Entry(
            frame,
            width=35
        )

        self.entry_port.grid(
            row=2,
            column=1,
            pady=5
        )

        self.entry_port.insert(
            0,
            "3306"
        )

        # -----------------------------------------------------
        # USUÁRIO
        # -----------------------------------------------------

        ttk.Label(
            frame,
            text="Usuário:"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=5
        )

        self.entry_user = ttk.Entry(
            frame,
            width=35
        )

        self.entry_user.grid(
            row=3,
            column=1,
            pady=5
        )

        self.entry_user.insert(
            0,
            "root"
        )

        # -----------------------------------------------------
        # SENHA
        # -----------------------------------------------------

        ttk.Label(
            frame,
            text="Senha:"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=5
        )

        self.entry_password = ttk.Entry(
            frame,
            width=35,
            show="*"
        )

        self.entry_password.grid(
            row=4,
            column=1,
            pady=5
        )

        # -----------------------------------------------------
        # BOTÃO TESTAR
        # -----------------------------------------------------

        ttk.Button(
            frame,
            text="Testar conexão",
            command=self.testar
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            pady=(20, 5)
        )

        # -----------------------------------------------------
        # BOTÃO CONFIGURAR
        # -----------------------------------------------------

        ttk.Button(
            frame,
            text="Salvar e configurar banco",
            command=self.configurar
        ).grid(
            row=6,
            column=0,
            columnspan=2,
            pady=5
        )

        self.label_status = ttk.Label(
            frame,
            text=""
        )

        self.label_status.grid(
            row=7,
            column=0,
            columnspan=2,
            pady=10
        )

    # =========================================================
    # OBTER DADOS
    # =========================================================

    def obter_dados(self):

        host = self.entry_host.get().strip()
        port = self.entry_port.get().strip()
        user = self.entry_user.get().strip()
        password = self.entry_password.get()

        if not host:
            raise ValueError(
                "Informe o servidor."
            )

        if not port:
            raise ValueError(
                "Informe a porta."
            )

        if not user:
            raise ValueError(
                "Informe o usuário."
            )

        try:
            port = int(port)
        except ValueError:
            raise ValueError(
                "A porta deve ser um número."
            )

        return (
            host,
            port,
            user,
            password
        )

    # =========================================================
    # TESTAR CONEXÃO
    # =========================================================

    def testar(self):

        try:

            (
                host,
                port,
                user,
                password
            ) = self.obter_dados()

            sucesso, mensagem = testar_conexao(
                host,
                port,
                user,
                password
            )

            if sucesso:

                self.label_status.configure(
                    text="✓ Conexão realizada com sucesso."
                )

                messagebox.showinfo(
                    "Conexão",
                    "Conexão com o MySQL realizada com sucesso.",
                    parent=self.janela
                )

            else:

                self.label_status.configure(
                    text="✗ Falha na conexão."
                )

                messagebox.showerror(
                    "Erro de conexão",
                    mensagem,
                    parent=self.janela
                )

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                str(erro),
                parent=self.janela
            )

    # =========================================================
    # CONFIGURAR
    # =========================================================

    def configurar(self):

        try:

            (
                host,
                port,
                user,
                password
            ) = self.obter_dados()

            # -------------------------------------------------
            # TESTA
            # -------------------------------------------------

            sucesso, mensagem = testar_conexao(
                host,
                port,
                user,
                password
            )

            if not sucesso:

                messagebox.showerror(
                    "Erro de conexão",
                    "Não foi possível conectar ao MySQL.\n\n"
                    + mensagem,
                    parent=self.janela
                )

                return

            # -------------------------------------------------
            # CRIA BANCO E TABELAS
            # -------------------------------------------------

            sucesso, mensagem = criar_banco_e_tabelas(
                host,
                port,
                user,
                password
            )

            if not sucesso:

                messagebox.showerror(
                    "Erro",
                    "Não foi possível criar o banco de dados.\n\n"
                    + mensagem,
                    parent=self.janela
                )

                return

            # -------------------------------------------------
            # SALVA CONFIGURAÇÃO
            # -------------------------------------------------

            salvar_config(
                host,
                port,
                user,
                password
            )

            self.configurado = True

            messagebox.showinfo(
                "Configuração concluída",
                "Banco de dados configurado com sucesso!",
                parent=self.janela
            )

            self.janela.destroy()

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                str(erro),
                parent=self.janela
            )