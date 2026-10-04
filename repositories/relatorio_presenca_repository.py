from database.connection import criar_conexao


def listar_turmas_disciplinas_relatorio():

    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT
            td.id AS turma_disciplina_id,
            t.id AS turma_id,
            t.nome AS turma,
            d.id AS disciplina_id,
            d.nome AS disciplina
        FROM turma_disciplinas td

        INNER JOIN turmas t
            ON t.id = td.turma_id

        INNER JOIN disciplinas d
            ON d.id = td.disciplina_id

        WHERE t.ativo = TRUE
          AND d.ativo = TRUE

        ORDER BY
            t.nome,
            d.nome
    """

    cursor.execute(sql)

    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()

    return resultado


def listar_alunos_relatorio(turma_id):

    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT
            a.id,
            a.nome,
            a.matricula

        FROM matriculas m

        INNER JOIN alunos a
            ON a.id = m.aluno_id

        WHERE m.turma_id = %s
          AND m.ativo = TRUE
          AND a.ativo = TRUE

        ORDER BY a.nome
    """

    cursor.execute(
        sql,
        (turma_id,)
    )

    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()

    return resultado


def gerar_relatorio_presenca(
    turma_disciplina_id
):

    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT
            au.id AS aula_id,
            au.data_aula,
            au.quantidade_horas_aula,

            a.id AS aluno_id,
            a.nome AS aluno,
            a.matricula,

            p.numero_hora_aula,
            p.status

        FROM aulas au

        INNER JOIN turma_disciplinas td
            ON td.id = au.turma_disciplina_id

        INNER JOIN matriculas m
            ON m.turma_id = td.turma_id
           AND m.ativo = TRUE

        INNER JOIN alunos a
            ON a.id = m.aluno_id
           AND a.ativo = TRUE

        LEFT JOIN presencas p
            ON p.aula_id = au.id
           AND p.aluno_id = a.id

        WHERE au.turma_disciplina_id = %s

        ORDER BY
            a.nome,
            au.data_aula,
            p.numero_hora_aula
    """

    cursor.execute(
        sql,
        (turma_disciplina_id,)
    )

    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()

    return resultado