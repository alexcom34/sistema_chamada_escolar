import traceback
import tkinter as tk
from tkinter import messagebox, ttk

from config import carregar_config
from database.initializer import criar_banco_e_tabelas
from views.config_banco_view import ConfigBancoView


def abrir_configuracao(janela):
    """
    Abre a tela de configuração do banco.
    Retorna True se o usuário configurou o banco.
    """
    print("Abrindo tela de configuração...")

    tela_config = ConfigBancoView(janela)

    janela.wait_window(tela_config.janela)

    print("Tela de configuração fechada.")
    print("Configurado:", tela_config.configurado)

    return tela_config.configurado


def verificar_banco(janela):
    """
    Verifica se existe configuração do banco.
    Se não existir, abre a tela de configuração.
    """
    print("Verificando configuração do banco...")

    config = carregar_config()

    print("Configuração encontrada:", config)

    # ============================================================
    # PRIMEIRA EXECUÇÃO
    # ============================================================
    if config is None:
        print("Nenhuma configuração encontrada.")
        print("Abrindo configuração inicial...")

        configurado = abrir_configuracao(janela)

        if not configurado:
            print("Configuração cancelada.")
            janela.destroy()
            return False

        print("Banco configurado com sucesso.")
        return True

    # ============================================================
    # CONFIGURAÇÃO JÁ EXISTE
    # ============================================================
    print("Configuração existente.")
    print("Testando banco de dados...")

    sucesso, mensagem = criar_banco_e_tabelas(
        config["host"],
        config["port"],
        config["user"],
        config["password"]
    )

    if sucesso:
        print("Banco conectado com sucesso.")
        return True

    # ============================================================
    # ERRO DE CONEXÃO
    # ============================================================
    resposta = messagebox.askyesno(
        "Erro de conexão",
        "Não foi possível conectar ao banco de dados.\n\n"
        + str(mensagem)
        + "\n\n"
        "Deseja abrir novamente a configuração do banco?",
        parent=janela
    )

    if resposta:
        configurado = abrir_configuracao(janela)
        if configurado:
            return True

    janela.destroy()
    return False


# ============================================================
# CRIAÇÃO DA JANELA PRINCIPAL
# ============================================================
try:
    print("=" * 60)
    print("INICIANDO SISTEMA DE CHAMADA")
    print("=" * 60)

    janela = tk.Tk()
    janela.title("Sistema de Chamada")
    janela.geometry("600x500")
    janela.resizable(False, False)

    print("Janela principal criada.")

    # ============================================================
    # INTERFACE
    # ============================================================
    titulo = ttk.Label(
        janela,
        text="Sistema de Chamada",
        font=("Arial", 20, "bold")
    )
    titulo.pack(pady=30)

    frame_menu = ttk.Frame(janela)
    frame_menu.pack()

    # ============================================================
    # FUNÇÕES DE ABERTURA
    # ============================================================
    def abrir_alunos():
        from views.alunos_view import AlunosView
        AlunosView(janela)

    def abrir_turmas():
        from views.turmas_view import TurmasView
        TurmasView(janela)

    def abrir_matriculas():
        from views.matriculas_view import MatriculasView
        MatriculasView(janela)

    def abrir_disciplinas():
        from views.disciplinas_view import DisciplinasView
        DisciplinasView(janela)

    def abrir_turma_disciplinas():
        from views.turma_disciplinas_view import TurmaDisciplinasView
        TurmaDisciplinasView(janela)

    def abrir_chamada():
        from views.chamada_view import ChamadaView
        ChamadaView(janela)

    def abrir_historico_chamadas():
        from views.historico_chamadas_view import HistoricoChamadasView
        HistoricoChamadasView(janela)

    def abrir_relatorios():
        from views.relatorios_view import RelatoriosView
        RelatoriosView(janela)

    def abrir_relatorio_presenca():
        from views.relatorio_presenca_view import RelatorioPresencaView
        RelatorioPresencaView(janela)

    def em_desenvolvimento():
        messagebox.showinfo(
            "Em desenvolvimento",
            "Esta funcionalidade será implementada nos próximos passos.",
            parent=janela
        )

    # ============================================================
    # BOTÕES
    # ============================================================
    ttk.Button(
        frame_menu,
        text="Alunos",
        width=25,
        command=abrir_alunos
    ).pack(pady=5)

    ttk.Button(
        frame_menu,
        text="Turmas",
        width=25,
        command=abrir_turmas
    ).pack(pady=5)

    ttk.Button(
        frame_menu,
        text="Matrículas",
        width=25,
        command=abrir_matriculas
    ).pack(pady=5)

    ttk.Button(
        frame_menu,
        text="Professores",
        width=25,
        command=em_desenvolvimento
    ).pack(pady=5)

    ttk.Button(
        frame_menu,
        text="Disciplinas",
        width=25,
        command=abrir_disciplinas
    ).pack(pady=5)

    ttk.Button(
        frame_menu,
        text="Disciplinas das Turmas",
        width=25,
        command=abrir_turma_disciplinas
    ).pack(pady=5)

    ttk.Button(
        frame_menu,
        text="Chamada",
        width=25,
        command=abrir_chamada
    ).pack(pady=5)

    ttk.Button(
        frame_menu,
        text="Histórico de Chamadas",
        width=25,
        command=abrir_historico_chamadas
    ).pack(pady=5)

    ttk.Button(
        frame_menu,
        text="Relatórios",
        width=25,
        command=abrir_relatorios
    ).pack(pady=5)

    ttk.Button(
        janela,
        text="Relatório Detalhado de Presença",
        width=30,
        command=abrir_relatorio_presenca
    ).pack(pady=10)

    # ============================================================
    # MOSTRA A JANELA PRINCIPAL
    # ============================================================
    janela.update()
    print("Interface principal criada.")

    # ============================================================
    # VERIFICA BANCO
    # ============================================================
    if not verificar_banco(janela):
        print("Sistema encerrado.")
        exit()

    print("Banco OK.")
    print("Iniciando mainloop...")

    # ============================================================
    # MAINLOOP
    # ============================================================
    janela.mainloop()

except Exception as erro:
    erro_completo = traceback.format_exc()

    print()
    print("=" * 70)
    print("ERRO AO INICIAR O SISTEMA")
    print("=" * 70)
    print(erro_completo)
    print("=" * 70)

    try:
        messagebox.showerror(
            "Erro ao iniciar o sistema",
            "O sistema não conseguiu iniciar.\n\n"
            + str(erro)
            + "\n\n"
            "Veja o terminal para obter os detalhes."
        )
    except Exception:
        pass