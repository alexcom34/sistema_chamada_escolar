from database.connection import criar_conexao


def relatorio_frequencia_turma_disciplina(
    turma_disciplina_id
):
    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT
            a.id AS aluno_id,
            a.nome AS aluno,
            a.matricula,

            COUNT(p.id) AS total_horas,

            COALESCE(
                SUM(
                    CASE
                        WHEN p.status = 'PRESENTE'
                        THEN 1
                        ELSE 0
                    END
                ),
                0
            ) AS presencas,

            COALESCE(
                SUM(
                    CASE
                        WHEN p.status = 'FALTA'
                        THEN 1
                        ELSE 0
                    END
                ),
                0
            ) AS faltas,

            COALESCE(
                SUM(
                    CASE
                        WHEN p.status = 'JUSTIFICADA'
                        THEN 1
                        ELSE 0
                    END
                ),
                0
            ) AS justificadas

        FROM matriculas m

        INNER JOIN alunos a
            ON a.id = m.aluno_id

        LEFT JOIN (
            SELECT
                p.aluno_id,
                p.status,
                p.id
            FROM presencas p

            INNER JOIN aulas au
                ON au.id = p.aula_id

            WHERE au.turma_disciplina_id = %s
        ) p
            ON p.aluno_id = a.id

        WHERE m.turma_id = (
            SELECT turma_id
            FROM turma_disciplinas
            WHERE id = %s
        )

        AND m.ativo = TRUE
        AND a.ativo = TRUE

        GROUP BY
            a.id,
            a.nome,
            a.matricula

        ORDER BY
            a.nome
    """

    cursor.execute(
        sql,
        (
            turma_disciplina_id,
            turma_disciplina_id
        )
    )

    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()

    return resultado