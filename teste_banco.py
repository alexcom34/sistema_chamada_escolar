from config import carregar_config

print("1 - Importou config")

config = carregar_config()

print("2 - Configuração encontrada:")
print(config)

from database.initializer import criar_banco_e_tabelas

print("3 - Importou initializer")

if config is None:
    print("4 - NÃO EXISTE configuração do banco.")
    print("O sistema deveria abrir a tela de configuração.")
else:
    print("4 - Tentando conectar ao MySQL...")

    sucesso, mensagem = criar_banco_e_tabelas(
        config["host"],
        config["port"],
        config["user"],
        config["password"]
    )

    print("5 - Resultado:")
    print("Sucesso:", sucesso)
    print("Mensagem:", mensagem)

input("\nPressione ENTER para fechar...")