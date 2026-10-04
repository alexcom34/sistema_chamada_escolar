from database.connection import criar_conexao


def vincular_disciplina(
    turma_id,
    disciplina_id,
    professor_id,
    aulas_previstas
):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO turma_disciplinas
        (
            turma_id,
            disciplina_id,
            professor_id,
            aulas_previstas
        )
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(
        sql,
        (
            turma_id,
            disciplina_id,
            professor_id,
            aulas_previstas
        )
    )

    conexao.commit()

    cursor.close()
    conexao.close()


def listar_disciplinas_da_turma(turma_id):
    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT
            td.id,
            d.nome AS disciplina,
            d.codigo,
            d.carga_horaria,
            d.minutos_hora_aula,
            p.nome AS professor,
            td.aulas_previstas
        FROM turma_disciplinas td

        INNER JOIN disciplinas d
            ON d.id = td.disciplina_id

        LEFT JOIN professores p
            ON p.id = td.professor_id

        WHERE td.turma_id = %s

        ORDER BY d.nome
    """

    cursor.execute(sql, (turma_id,))

    disciplinas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return disciplinas

def buscar_turma_da_disciplina(turma_disciplina_id):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    sql = """
        SELECT turma_id
        FROM turma_disciplinas
        WHERE id = %s
    """

    cursor.execute(
        sql,
        (turma_disciplina_id,)
    )

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    if resultado is None:
        return None

    return resultado[0]


def disciplina_ja_vinculada(turma_id, disciplina_id):
    
    conexao = criar_conexao()
    cursor = conexao.cursor()

    sql = """
        SELECT id
        FROM turma_disciplinas
        WHERE turma_id = %s
          AND disciplina_id = %s
    """

    cursor.execute(
        sql,
        (turma_id, disciplina_id)
    )

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado is not None