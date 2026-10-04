import json
import os

NOME_ARQUIVO_CONFIG = "config_banco.json"
NOME_PASTA_APP = "SistemaChamada"


def pasta_config():
    """
    Retorna a pasta de configuração do usuário.
    Exemplo:
    C:\\Users\\Usuario\\AppData\\Roaming\\SistemaChamada
    """
    appdata = os.getenv("APPDATA")

    if not appdata:
        appdata = os.path.expanduser("~")

    pasta = os.path.join(appdata, NOME_PASTA_APP)
    os.makedirs(pasta, exist_ok=True)

    return pasta


def caminho_config():
    """
    Retorna o caminho completo do arquivo de configuração.
    """
    return os.path.join(pasta_config(), NOME_ARQUIVO_CONFIG)


def carregar_config():
    """
    Carrega a configuração do banco.
    Retorna:
        dict -> configuração encontrada
        None -> configuração inexistente ou inválida
    """
    arquivo = caminho_config()

    if not os.path.exists(arquivo):
        return None

    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)

        # Verificação básica
        campos_obrigatorios = ["host", "port", "user", "password", "database"]

        for campo in campos_obrigatorios:
            if campo not in dados:
                return None

        return dados

    except Exception:
        return None


def salvar_config(host, port, user, password):
    """
    Salva a configuração do banco no AppData do usuário.
    """
    dados = {
        "host": host,
        "port": int(port),
        "user": user,
        "password": password,
        "database": "sistema_chamada",
    }

    arquivo = caminho_config()

    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


# Mantido por compatibilidade com outros arquivos do projeto.
DB_CONFIG = carregar_config()