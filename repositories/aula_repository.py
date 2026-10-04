from database.connection import criar_conexao


def registrar_aula(
    turma_disciplina_id,
    data_aula,
    quantidade_horas_aula,
    observacao=None
):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO aulas
        (turma_disciplina_id, data_aula, quantidade_horas_aula, observacao)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(
        sql,
        (
            turma_disciplina_id,
            data_aula,
            quantidade_horas_aula,
            observacao
        )
    )

    aula_id = cursor.lastrowid

    conexao.commit()

    cursor.close()
    conexao.close()

    return aula_id


def buscar_aula(turma_disciplina_id, data_aula):

    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT
            id,
            turma_disciplina_id,
            data_aula,
            quantidade_horas_aula,
            observacao
        FROM aulas
        WHERE turma_disciplina_id = %s
          AND data_aula = %s
    """

    cursor.execute(
        sql,
        (
            turma_disciplina_id,
            data_aula
        )
    )

    aula = cursor.fetchone()

    cursor.close()
    conexao.close()

    return aula


def listar_aulas():

    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT
            a.id,
            a.data_aula,
            a.quantidade_horas_aula,
            a.observacao,
            t.nome AS turma,
            d.nome AS disciplina,
            p.nome AS professor
        FROM aulas a

        INNER JOIN turma_disciplinas td
            ON td.id = a.turma_disciplina_id

        INNER JOIN turmas t
            ON t.id = td.turma_id

        INNER JOIN disciplinas d
            ON d.id = td.disciplina_id

        LEFT JOIN professores p
            ON p.id = td.professor_id

        ORDER BY
            a.data_aula DESC,
            t.nome,
            d.nome
    """

    cursor.execute(sql)

    aulas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return aulas


def buscar_aula_por_id(aula_id):

    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT
            a.id,
            a.data_aula,
            a.quantidade_horas_aula,
            a.observacao,
            t.nome AS turma,
            d.nome AS disciplina,
            p.nome AS professor
        FROM aulas a

        INNER JOIN turma_disciplinas td
            ON td.id = a.turma_disciplina_id

        INNER JOIN turmas t
            ON t.id = td.turma_id

        INNER JOIN disciplinas d
            ON d.id = td.disciplina_id

        LEFT JOIN professores p
            ON p.id = td.professor_id

        WHERE a.id = %s
    """

    cursor.execute(
        sql,
        (aula_id,)
    )

    aula = cursor.fetchone()

    cursor.close()
    conexao.close()

    return aula