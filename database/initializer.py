import mysql.connector
from mysql.connector import Error


def testar_conexao(
    host,
    port,
    user,
    password
):

    conexao = None

    try:

        conexao = mysql.connector.connect(
            host=host,
            port=int(port),
            user=user,
            password=password
        )

        if conexao.is_connected():
            return True, "Conexão realizada com sucesso."

        return False, "Não foi possível conectar ao MySQL."

    except Error as erro:

        return False, str(erro)

    finally:

        if conexao and conexao.is_connected():
            conexao.close()


def criar_banco_e_tabelas(
    host,
    port,
    user,
    password
):

    conexao = None
    cursor = None

    try:

        # =====================================================
        # CONECTA AO MYSQL
        # =====================================================

        conexao = mysql.connector.connect(
            host=host,
            port=int(port),
            user=user,
            password=password
        )

        cursor = conexao.cursor()

        # =====================================================
        # CRIA O BANCO
        # =====================================================

        cursor.execute("""
            CREATE DATABASE IF NOT EXISTS sistema_chamada
            CHARACTER SET utf8mb4
            COLLATE utf8mb4_unicode_ci
        """)

        cursor.close()
        conexao.close()

        # =====================================================
        # CONECTA AO BANCO
        # =====================================================

        conexao = mysql.connector.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database="sistema_chamada"
        )

        cursor = conexao.cursor()

        # =====================================================
        # PROFESSORES
        # =====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS professores (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(150) NOT NULL,
                email VARCHAR(150),
                ativo BOOLEAN DEFAULT TRUE
            )
        """)

        # =====================================================
        # TURMAS
        # =====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS turmas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                codigo VARCHAR(50) UNIQUE,
                ano INT NOT NULL,
                semestre INT NOT NULL,
                professor_id INT,
                ativo BOOLEAN DEFAULT TRUE,

                FOREIGN KEY (professor_id)
                    REFERENCES professores(id)
            )
        """)

        # =====================================================
        # ALUNOS
        # =====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(150) NOT NULL,
                matricula VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(150),
                ativo BOOLEAN DEFAULT TRUE
            )
        """)

        # =====================================================
        # MATRÍCULAS
        # =====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS matriculas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                aluno_id INT NOT NULL,
                turma_id INT NOT NULL,
                data_matricula DATE NOT NULL,
                ativo BOOLEAN DEFAULT TRUE,

                UNIQUE (aluno_id, turma_id),

                FOREIGN KEY (aluno_id)
                    REFERENCES alunos(id),

                FOREIGN KEY (turma_id)
                    REFERENCES turmas(id)
            )
        """)

        # =====================================================
        # DISCIPLINAS
        # =====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS disciplinas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(150) NOT NULL,
                codigo VARCHAR(50),
                carga_horaria DECIMAL(6,2) NOT NULL,
                minutos_hora_aula INT NOT NULL DEFAULT 50,
                ativo BOOLEAN DEFAULT TRUE
            )
        """)

        # =====================================================
        # TURMA x DISCIPLINAS
        # =====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS turma_disciplinas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                turma_id INT NOT NULL,
                disciplina_id INT NOT NULL,
                professor_id INT,
                aulas_previstas INT NOT NULL,

                UNIQUE (turma_id, disciplina_id),

                FOREIGN KEY (turma_id)
                    REFERENCES turmas(id),

                FOREIGN KEY (disciplina_id)
                    REFERENCES disciplinas(id),

                FOREIGN KEY (professor_id)
                    REFERENCES professores(id)
            )
        """)

        # =====================================================
        # AULAS
        # =====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS aulas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                turma_disciplina_id INT NOT NULL,
                data_aula DATE NOT NULL,
                quantidade_horas_aula DECIMAL(4,2)
                    NOT NULL DEFAULT 1,
                observacao VARCHAR(255),

                FOREIGN KEY (turma_disciplina_id)
                    REFERENCES turma_disciplinas(id)
            )
        """)

        # =====================================================
        # PRESENÇAS
        # =====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS presencas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                aula_id INT NOT NULL,
                aluno_id INT NOT NULL,
                numero_hora_aula INT NOT NULL DEFAULT 1,

                status ENUM(
                    'PRESENTE',
                    'FALTA',
                    'JUSTIFICADA'
                ) NOT NULL DEFAULT 'PRESENTE',

                UNIQUE (
                    aula_id,
                    aluno_id,
                    numero_hora_aula
                ),

                FOREIGN KEY (aula_id)
                    REFERENCES aulas(id),

                FOREIGN KEY (aluno_id)
                    REFERENCES alunos(id)
            )
        """)

        conexao.commit()

        return True, "Banco configurado com sucesso."

    except Error as erro:

        if conexao:
            conexao.rollback()

        return False, str(erro)

    except Exception as erro:

        if conexao:
            conexao.rollback()

        return False, str(erro)

    finally:

        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()