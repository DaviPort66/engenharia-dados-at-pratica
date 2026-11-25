from relacional import usuario, professor, turma, leciona


# ---------- entrada de dados ----------
def ask(msg, conv=str, obrigatorio=False):
    """Lê um valor. Enter vazio => None (ou erro, se obrigatório)."""
    txt = input(msg).strip()
    if not txt:
        if obrigatorio:
            raise ValueError("Campo obrigatório.")
        return None
    try:
        return conv(txt)
    except ValueError:
        raise ValueError(f"Valor inválido: '{txt}'.")


def pedir_lista(msg):
    return [x.strip() for x in input(msg).split(",") if x.strip()]


def mostrar(linhas):
    if not linhas:
        print("  Nenhum registro encontrado.")
    for l in linhas:
        print(" ", l)


def efeito(rotulo, consulta, *args):
    """Consulta o banco e mostra o estado atual do registro."""
    print(f"  [banco | {rotulo}]")
    mostrar(consulta(*args))


def coletar(campos):
    out = {}
    for col, msg, conv in campos:
        v = ask(f"{msg} (Enter mantém): ", conv)
        if v is not None:
            out[col] = v
    return out


def rodar_menu(titulo, acoes):
    while True:
        print(f"\n--- {titulo} ---")
        for k, (nome, _) in acoes.items():
            print(f"{k}) {nome}")
        print("0) Voltar")
        op = input("Opção: ").strip()
        if op == "0":
            return
        if op not in acoes:
            print("Opção inválida.")
            continue
        try:
            acoes[op][1]()
        except ValueError as e:
            print(f"Erro: {e}")


# ---------- usuário ----------
def u_inserir():
    cpf = ask("CPF (só números): ", int, True)
    nome = ask("Nome: ", obrigatorio=True)
    nasc = ask("Data de nascimento (AAAA-MM-DD, opcional): ")
    emails = pedir_lista("E-mails (separados por vírgula): ")
    tels = pedir_lista("Telefones (separados por vírgula): ")
    login = ask("Login: ")
    senha = ask("Senha: ")
    efeito("antes", usuario.buscar, cpf)
    n = usuario.inserir(cpf, nome, nasc, emails, tels, login, senha)
    print(f"OK: {n} usuário inserido.")
    efeito("depois", usuario.buscar, cpf)


def u_atualizar():
    cpf = ask("CPF do usuário: ", int, True)
    campos = coletar([("nome", "Novo nome", str), ("data_nascimento", "Nova data (AAAA-MM-DD)", str),
                      ("login", "Novo login", str), ("senha", "Nova senha", str)])
    emails = pedir_lista("Novos e-mails (Enter mantém): ")
    if emails: campos["email"] = emails
    tels = pedir_lista("Novos telefones (Enter mantém): ")
    if tels: campos["telefone"] = tels
    efeito("antes", usuario.buscar, cpf)
    n = usuario.atualizar(cpf, campos)
    print(f"OK: {n} usuário atualizado." if n else "Nenhum usuário com esse CPF.")
    efeito("depois", usuario.buscar, cpf)


def u_deletar():
    cpf = ask("CPF do usuário: ", int, True)
    efeito("antes", usuario.buscar, cpf)
    n = usuario.deletar(cpf)
    print(f"OK: {n} usuário removido." if n else "Nenhum usuário com esse CPF.")
    efeito("depois", usuario.buscar, cpf)


# ---------- professor ----------
def p_inserir():
    print("Formação: Graduação, Especialização, Mestrado, Doutorado | Jornada: 20h, 40h, DE")
    mat = ask("Matrícula (até 7 caracteres): ", obrigatorio=True)
    cpf = ask("CPF do usuário (opcional): ", int)
    depto = ask("Departamento (ex.: DCOMP): ")
    formacao = ask("Formação: ")
    data_adm = ask("Data de admissão (AAAA-MM-DD): ")
    jornada = ask("Jornada: ")
    salario = ask("Salário: ", float)
    efeito("antes", professor.buscar, mat)
    n = professor.inserir(mat, cpf, depto, formacao, data_adm, jornada, salario)
    print(f"OK: {n} professor inserido.")
    efeito("depois", professor.buscar, mat)


def p_atualizar():
    mat = ask("Matrícula do professor: ", obrigatorio=True)
    campos = coletar([("cpf", "Novo CPF", int), ("departamento", "Novo departamento", str),
                      ("formacao", "Nova formação", str), ("data_admissao", "Nova data de admissão", str),
                      ("tipo_jornada_trabalho", "Nova jornada (20h/40h/DE)", str),
                      ("salario", "Novo salário", float)])
    efeito("antes", professor.buscar, mat)
    n = professor.atualizar(mat, campos)
    print(f"OK: {n} professor atualizado." if n else "Nenhum professor com essa matrícula.")
    efeito("depois", professor.buscar, mat)


def p_deletar():
    mat = ask("Matrícula do professor: ", obrigatorio=True)
    efeito("antes", professor.buscar, mat)
    n = professor.deletar(mat)
    print(f"OK: {n} professor removido." if n else "Nenhum professor com essa matrícula.")
    efeito("depois", professor.buscar, mat)


# ---------- turma ----------
def t_inserir():
    cod = ask("Código da disciplina (ex.: COMP0123): ", obrigatorio=True)
    numero = ask("Número da turma: ", int, True)
    ano = ask("Ano: ", int, True)
    semestre = ask("Semestre (1 ou 2): ", int, True)
    print(f"  [banco | antes] {len(turma.listar())} turmas cadastradas")
    id_nova = turma.inserir(cod, numero, ano, semestre)
    print(f"OK: turma inserida com id_turma = {id_nova}.")
    print(f"  [banco | depois] {len(turma.listar())} turmas cadastradas")
    efeito("nova turma", turma.buscar, id_nova)


def t_atualizar():
    id_t = ask("id_turma: ", int, True)
    campos = coletar([("cod_disc", "Nova disciplina", str), ("numero", "Novo número", int),
                      ("ano", "Novo ano", int), ("semestre", "Novo semestre", int)])
    efeito("antes", turma.buscar, id_t)
    n = turma.atualizar(id_t, campos)
    print(f"OK: {n} turma atualizada." if n else "Nenhuma turma com esse id.")
    efeito("depois", turma.buscar, id_t)


def t_deletar():
    print("Atenção: apagar a turma também apaga seus registros em leciona e cursa (CASCADE).")
    id_t = ask("id_turma: ", int, True)
    efeito("turma - antes", turma.buscar, id_t)
    efeito("leciona dessa turma - antes", leciona.buscar_por_turma, id_t)
    n = turma.deletar(id_t)
    print(f"OK: {n} turma removida." if n else "Nenhuma turma com esse id.")
    efeito("turma - depois", turma.buscar, id_t)
    efeito("leciona dessa turma - depois", leciona.buscar_por_turma, id_t)


# ---------- leciona ----------
def l_inserir():
    id_t = ask("id_turma: ", int, True)
    mat = ask("Matrícula do professor: ", obrigatorio=True)
    efeito("antes", leciona.buscar_por_turma, id_t)
    n = leciona.inserir(id_t, mat)
    print(f"OK: {n} vínculo inserido.")
    efeito("depois", leciona.buscar_por_turma, id_t)


def l_trocar():
    id_t = ask("id_turma: ", int, True)
    atual = ask("Matrícula atual: ", obrigatorio=True)
    novo = ask("Nova matrícula: ", obrigatorio=True)
    efeito("antes", leciona.buscar_por_turma, id_t)
    n = leciona.trocar_professor(id_t, atual, novo)
    print(f"OK: {n} vínculo atualizado." if n else "Vínculo não encontrado.")
    efeito("depois", leciona.buscar_por_turma, id_t)


def l_deletar():
    id_t = ask("id_turma: ", int, True)
    mat = ask("Matrícula do professor: ", obrigatorio=True)
    efeito("antes", leciona.buscar_por_turma, id_t)
    n = leciona.deletar(id_t, mat)
    print(f"OK: {n} vínculo removido." if n else "Vínculo não encontrado.")
    efeito("depois", leciona.buscar_por_turma, id_t)


MENUS = {
    "1": ("Usuário", {
        "1": ("Inserir", u_inserir),
        "2": ("Listar", lambda: mostrar(usuario.listar())),
        "3": ("Buscar por CPF", lambda: mostrar(usuario.buscar(ask("CPF: ", int, True)))),
        "4": ("Atualizar", u_atualizar),
        "5": ("Deletar", u_deletar)}),
    "2": ("Professor", {
        "1": ("Inserir", p_inserir),
        "2": ("Listar", lambda: mostrar(professor.listar())),
        "3": ("Buscar por matrícula", lambda: mostrar(professor.buscar(ask("Matrícula: ", obrigatorio=True)))),
        "4": ("Atualizar", p_atualizar),
        "5": ("Deletar", p_deletar)}),
    "3": ("Turma", {
        "1": ("Inserir", t_inserir),
        "2": ("Listar", lambda: mostrar(turma.listar())),
        "3": ("Buscar por id", lambda: mostrar(turma.buscar(ask("id_turma: ", int, True)))),
        "4": ("Atualizar", t_atualizar),
        "5": ("Deletar", t_deletar)}),
    "4": ("Leciona", {
        "1": ("Inserir (professor em turma)", l_inserir),
        "2": ("Listar", lambda: mostrar(leciona.listar())),
        "3": ("Buscar por turma", lambda: mostrar(leciona.buscar_por_turma(ask("id_turma: ", int, True)))),
        "4": ("Trocar professor da turma", l_trocar),
        "5": ("Deletar", l_deletar)}),
}


def main():
    while True:
        print("\n=== CRUD UNIVERSIDADE ===")
        for k, (nome, _) in MENUS.items():
            print(f"{k}) {nome}")
        print("0) Sair")
        op = input("Opção: ").strip()
        if op == "0":
            break
        if op in MENUS:
            rodar_menu(MENUS[op][0].upper(), MENUS[op][1])
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
