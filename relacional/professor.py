from relacional.conexao import executar, atualizar_campos

EDITAVEIS = {"cpf", "departamento", "formacao", "data_admissao",
             "tipo_jornada_trabalho", "salario"}

SELECT = """SELECT p.mat_professor, u.nome, p.cpf, p.departamento, p.formacao,
                   p.data_admissao, p.tipo_jornada_trabalho, p.salario
            FROM professor p LEFT JOIN usuario u ON u.cpf = p.cpf"""


def inserir(mat, cpf, depto, formacao, data_adm, jornada, salario):
    sql = """INSERT INTO professor (mat_professor, cpf, departamento, formacao,
                                    data_admissao, tipo_jornada_trabalho, salario)
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    return executar(sql, (mat, cpf, depto, formacao, data_adm, jornada, salario))


def listar():
    return executar(SELECT + " ORDER BY p.mat_professor", fetch=True)


def buscar(mat):
    return executar(SELECT + " WHERE p.mat_professor = %s", (mat,), fetch=True)


def atualizar(mat, campos):
    return atualizar_campos("professor", campos, EDITAVEIS, "mat_professor = %s", (mat,))


def deletar(mat):
    return executar("DELETE FROM professor WHERE mat_professor = %s", (mat,))
