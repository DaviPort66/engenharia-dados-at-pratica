from relacional.conexao import executar

SELECT = """SELECT l.id_turma, t.cod_disc, t.numero, t.ano, t.semestre,
                   l.mat_professor, u.nome AS professor
            FROM leciona l
            JOIN turma t ON t.id_turma = l.id_turma
            JOIN professor p ON p.mat_professor = l.mat_professor
            LEFT JOIN usuario u ON u.cpf = p.cpf"""


def inserir(id_turma, mat_professor):
    return executar("INSERT INTO leciona (id_turma, mat_professor) VALUES (%s, %s)",
                    (id_turma, mat_professor))


def listar():
    return executar(SELECT + " ORDER BY l.id_turma, l.mat_professor", fetch=True)


def buscar_por_turma(id_turma):
    return executar(SELECT + " WHERE l.id_turma = %s", (id_turma,), fetch=True)


def trocar_professor(id_turma, mat_atual, mat_novo):
    return executar("""UPDATE leciona SET mat_professor = %s
                       WHERE id_turma = %s AND mat_professor = %s""",
                    (mat_novo, id_turma, mat_atual))


def deletar(id_turma, mat_professor):
    return executar("DELETE FROM leciona WHERE id_turma = %s AND mat_professor = %s",
                    (id_turma, mat_professor))
