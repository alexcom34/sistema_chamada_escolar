from database.connection import criar_conexao


def cadastrar_professor(nome, email=None):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO professores (nome, email)
        VALUES (%s, %s)
    """

    cursor.execute(sql, (nome, email))
    conexao.commit()

    cursor.close()
    conexao.close()


def listar_professores():
    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, nome, email, ativo
        FROM professores
        WHERE ativo = TRUE
        ORDER BY nome
    """)

    professores = cursor.fetchall()

    cursor.close()
    conexao.close()

    return professores