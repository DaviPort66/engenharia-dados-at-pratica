import hashlib
from relacional.conexao import executar

COLUNAS_EDITAVEIS = {"nome", "data_nascimento", "email", "telefone", "login", "senha"}


def _hash(senha):
    # A coluna senha é VARCHAR(32): um MD5 em hexadecimal tem exatamente 32 caracteres.
    return hashlib.md5(senha.encode()).hexdigest()


def inserir(cpf, nome, data_nascimento, emails, telefones, login, senha):
    sql = """INSERT INTO usuario (cpf, nome, data_nascimento, email, telefone, login, senha)
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    return executar(sql, (cpf, nome, data_nascimento or None, emails, telefones,
                          login or None, _hash(senha) if senha else None))


def listar():
    return executar("""SELECT cpf, nome, data_nascimento, email, telefone, login
                       FROM usuario ORDER BY nome""", fetch=True)


def buscar(cpf):
    return executar("""SELECT cpf, nome, data_nascimento, email, telefone, login
                       FROM usuario WHERE cpf = %s""", (cpf,), fetch=True)


def atualizar(cpf, campos):
    campos = {k: v for k, v in campos.items() if k in COLUNAS_EDITAVEIS}
    if not campos:
        raise ValueError("Nenhum campo para atualizar.")
    if "senha" in campos:
        campos["senha"] = _hash(campos["senha"])
    sets = ", ".join(f"{col} = %s" for col in campos)
    return executar(f"UPDATE usuario SET {sets} WHERE cpf = %s", (*campos.values(), cpf))


def deletar(cpf):
    return executar("DELETE FROM usuario WHERE cpf = %s", (cpf,))
