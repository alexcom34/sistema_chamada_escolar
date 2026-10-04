from database.connection import criar_conexao


def cadastrar_disciplina(
    nome,
    codigo,
    carga_horaria,
    minutos_hora_aula=50
):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO disciplinas
        (
            nome,
            codigo,
            carga_horaria,
            minutos_hora_aula
        )
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(
        sql,
        (
            nome,
            codigo,
            carga_horaria,
            minutos_hora_aula
        )
    )

    conexao.commit()

    cursor.close()
    conexao.close()


def listar_disciplinas():
    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            nome,
            codigo,
            carga_horaria,
            minutos_hora_aula,
            ativo
        FROM disciplinas
        WHERE ativo = TRUE
        ORDER BY nome
    """)

    disciplinas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return disciplinas