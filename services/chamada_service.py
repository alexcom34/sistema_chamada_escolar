from database.connection import criar_conexao

from repositories.aula_repository import (
    buscar_aula
)

from repositories.turma_disciplina_repository import (
    buscar_turma_da_disciplina
)

from repositories.matricula_repository import (
    aluno_pertence_turma
)


def registrar_chamada(
    turma_disciplina_id,
    data_aula,
    quantidade_horas_aula,
    presencas,
    observacao=None
):

    # --------------------------------
    # 1. Verificar se a disciplina existe
    # --------------------------------

    turma_id = buscar_turma_da_disciplina(
        turma_disciplina_id
    )

    if turma_id is None:
        raise ValueError(
            "A turma/disciplina não existe."
        )


    # --------------------------------
    # 2. Verificar chamada duplicada
    # --------------------------------

    aula_existente = buscar_aula(
        turma_disciplina_id,
        data_aula
    )

    if aula_existente is not None:
        raise ValueError(
            "Já existe uma chamada registrada "
            "para essa disciplina nessa data."
        )


    # --------------------------------
    # 3. Validar alunos e horas-aula
    # --------------------------------

    for presenca in presencas:

        aluno_id = presenca["aluno_id"]

        pertence = aluno_pertence_turma(
            aluno_id,
            turma_id
        )

        if not pertence:
            raise ValueError(
                f"O aluno {aluno_id} "
                f"não pertence à turma."
            )

        hora = presenca["hora"]

        if hora < 1 or hora > quantidade_horas_aula:
            raise ValueError(
                f"A hora-aula {hora} é inválida. "
                f"Essa aula possui {quantidade_horas_aula} horas-aula."
            )


    # --------------------------------
    # 4. Criar conexão/transação
    # --------------------------------

    conexao = criar_conexao()
    cursor = conexao.cursor()

    try:

        # --------------------------------
        # 5. Criar aula
        # --------------------------------

        sql_aula = """
            INSERT INTO aulas
            (
                turma_disciplina_id,
                data_aula,
                quantidade_horas_aula,
                observacao
            )
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            sql_aula,
            (
                turma_disciplina_id,
                data_aula,
                quantidade_horas_aula,
                observacao
            )
        )

        aula_id = cursor.lastrowid


        # --------------------------------
        # 6. Registrar presenças (com hora/aula)
        # --------------------------------

        sql_presenca = """
            INSERT INTO presencas
            (
                aula_id,
                aluno_id,
                numero_hora_aula,
                status
            )
            VALUES (%s, %s, %s, %s)
        """

        for presenca in presencas:

            cursor.execute(
                sql_presenca,
                (
                    aula_id,
                    presenca["aluno_id"],
                    presenca["hora"],
                    presenca["status"]
                )
            )


        # --------------------------------
        # 7. Confirmar tudo
        # --------------------------------

        conexao.commit()

        return aula_id


    except Exception:

        # --------------------------------
        # 8. Desfazer tudo em caso de falha
        # --------------------------------

        conexao.rollback()

        raise


    finally:

        cursor.close()
        conexao.close()