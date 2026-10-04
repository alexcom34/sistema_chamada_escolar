import mysql.connector
from config import carregar_config


def criar_conexao():
    config = carregar_config()

    if not config:
        raise RuntimeError(
            "Banco de dados ainda não foi configurado."
        )

    return mysql.connector.connect(
        host=config["host"],
        port=int(config["port"]),
        user=config["user"],
        password=config["password"],
        database=config["database"]
    )