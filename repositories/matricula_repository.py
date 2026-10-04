from database.connection import criar_conexao


def matricular_aluno(aluno_id, turma_id):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO matriculas
        (aluno_id, turma_id, data_matricula)
        VALUES (%s, %s, CURDATE())
    """

    cursor.execute(
        sql,
        (aluno_id, turma_id)
    )

    conexao.commit()

    cursor.close()
    conexao.close()


def listar_alunos_da_turma(turma_id):
    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT
            a.id,
            a.nome,
            a.matricula,
            m.data_matricula
        FROM matriculas m
        INNER JOIN alunos a
            ON a.id = m.aluno_id
        WHERE m.turma_id = %s
          AND m.ativo = TRUE
          AND a.ativo = TRUE
        ORDER BY a.nome
    """

    cursor.execute(sql, (turma_id,))

    alunos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return alunos


def remover_aluno_da_turma(aluno_id, turma_id):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    sql = """
        UPDATE matriculas
        SET ativo = FALSE
        WHERE aluno_id = %s
          AND turma_id = %s
    """

    cursor.execute(
        sql,
        (aluno_id, turma_id)
    )

    conexao.commit()

    cursor.close()
    conexao.close()
    
def aluno_pertence_turma(aluno_id, turma_id):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    sql = """
        SELECT id
        FROM matriculas
        WHERE aluno_id = %s
          AND turma_id = %s
          AND ativo = TRUE
    """

    cursor.execute(
        sql,
        (
            aluno_id,
            turma_id
        )
    )

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado is not None