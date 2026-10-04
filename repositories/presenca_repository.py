from database.connection import criar_conexao


def registrar_presenca(
    cursor,
    aula_id,
    aluno_id,
    numero_hora_aula,
    status
):
    sql = """
        INSERT INTO presencas
        (
            aula_id,
            aluno_id,
            numero_hora_aula,
            status
        )
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(
        sql,
        (
            aula_id,
            aluno_id,
            numero_hora_aula,
            status
        )
    )


def listar_presencas_da_aula(aula_id):

    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT
            p.id,
            p.aula_id,
            p.aluno_id,
            a.nome AS aluno,
            a.matricula,
            p.numero_hora_aula,
            p.status
        FROM presencas p

        INNER JOIN alunos a
            ON a.id = p.aluno_id

        WHERE p.aula_id = %s

        ORDER BY
            a.nome,
            p.numero_hora_aula
    """

    cursor.execute(
        sql,
        (aula_id,)
    )

    presencas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return presencas