from database.connection import criar_conexao


def cadastrar_aluno(nome, matricula, email=None):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO alunos (nome, matricula, email)
        VALUES (%s, %s, %s)
    """

    cursor.execute(sql, (nome, matricula, email))
    conexao.commit()

    cursor.close()
    conexao.close()


def listar_alunos():
    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, nome, matricula, email, ativo
        FROM alunos
        WHERE ativo = TRUE
        ORDER BY nome
    """)

    alunos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return alunos


def buscar_aluno(id_aluno):
    conexao = criar_conexao()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, nome, matricula, email, ativo
        FROM alunos
        WHERE id = %s
    """, (id_aluno,))

    aluno = cursor.fetchone()

    cursor.close()
    conexao.close()

    return aluno


def atualizar_aluno(id_aluno, nome, matricula, email):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    sql = """
        UPDATE alunos
        SET nome = %s,
            matricula = %s,
            email = %s
        WHERE id = %s
    """

    cursor.execute(
        sql,
        (nome, matricula, email, id_aluno)
    )

    conexao.commit()

    cursor.close()
    conexao.close()


def excluir_aluno(id_aluno):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE alunos
        SET ativo = FALSE
        WHERE id = %s
    """, (id_aluno,))

    conexao.commit()

    cursor.close()
    conexao.close()