from relacional.conexao import executar, atualizar_campos

EDITAVEIS = {"cod_disc", "numero", "ano", "semestre"}

SELECT = """SELECT t.id_turma, t.cod_disc, d.nome AS disciplina, t.numero, t.ano, t.semestre
            FROM turma t JOIN disciplina d ON d.cod_disc = t.cod_disc"""


def inserir(cod_disc, numero, ano, semestre):
    sql = """INSERT INTO turma (cod_disc, numero, ano, semestre)
             VALUES (%s, %s, %s, %s) RETURNING id_turma"""
    return executar(sql, (cod_disc, numero, ano, semestre), fetch=True)[0][0]


def listar():
    return executar(SELECT + " ORDER BY t.ano, t.semestre, t.cod_disc, t.numero", fetch=True)


def buscar(id_turma):
    return executar(SELECT + " WHERE t.id_turma = %s", (id_turma,), fetch=True)


def atualizar(id_turma, campos):
    return atualizar_campos("turma", campos, EDITAVEIS, "id_turma = %s", (id_turma,))


def deletar(id_turma):
    return executar("DELETE FROM turma WHERE id_turma = %s", (id_turma,))
