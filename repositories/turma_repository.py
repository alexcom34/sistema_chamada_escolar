from database.connection import criar_conexao


def cadastrar_turma(nome, codigo, ano, semestre, professor_id=None):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO turmas
        (nome, codigo, ano, semestre, professor_id)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(
        sql,
        (nome, codigo, ano, semestre, professor_id)
    )

    conexao.commit()

    cursor.close()
    conexao.close()


def listar_turmas():
    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            nome,
            codigo,
            ano,
            semestre,
            professor_id,
            ativo
        FROM turmas
        WHERE ativo = TRUE
        ORDER BY ano DESC, semestre DESC, nome
    """)

    turmas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return turmas


def buscar_turma(id_turma):
    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            nome,
            codigo,
            ano,
            semestre,
            professor_id,
            ativo
        FROM turmas
        WHERE id = %s
    """, (id_turma,))

    turma = cursor.fetchone()

    cursor.close()
    conexao.close()

    return turma


def atualizar_turma(
    id_turma,
    nome,
    codigo,
    ano,
    semestre
):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    sql = """
        UPDATE turmas
        SET nome = %s,
            codigo = %s,
            ano = %s,
            semestre = %s
        WHERE id = %s
    """

    cursor.execute(
        sql,
        (nome, codigo, ano, semestre, id_turma)
    )

    conexao.commit()

    cursor.close()
    conexao.close()


def inativar_turma(id_turma):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE turmas
        SET ativo = FALSE
        WHERE id = %s
    """, (id_turma,))

    conexao.commit()

    cursor.close()
    conexao.close()