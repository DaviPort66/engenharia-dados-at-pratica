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
        print("Nenhum registro encontrado.")
    for l in linhas:
        print(l)


def coletar(campos):
    """campos: lista de (coluna, pergunta, conversor). Retorna só os preenchidos."""
    out = {}
    for col, msg, conv in campos:
        v = ask(f"{msg} (Enter mantém): ", conv)
        if v is not None:
            out[col] = v
    return out


def rodar_menu(titulo, acoes):
    """acoes: dict {'1': ('Descrição', função)}"""
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


def resultado(n, ok, vazio):
    print(f"OK: {ok}" if n else vazio)


# ---------- usuário ----------
def u_inserir():
    n = usuario.inserir(ask("CPF (só números): ", int, True), ask("Nome: ", obrigatorio=True),
                        ask("Data de nascimento (AAAA-MM-DD, opcional): "),
                        pedir_lista("E-mails (separados por vírgula): "),
                        pedir_lista("Telefones (separados por vírgula): "),
                        ask("Login: "), ask("Senha: "))
    print(f"OK: {n} usuário inserido.")


def u_atualizar():
    cpf = ask("CPF do usuário: ", int, True)
    campos = coletar([("nome", "Novo nome", str), ("data_nascimento", "Nova data (AAAA-MM-DD)", str),
                      ("login", "Novo login", str), ("senha", "Nova senha", str)])
    emails = pedir_lista("Novos e-mails (Enter mantém): ")
    if emails: campos["email"] = emails
    tels = pedir_lista("Novos telefones (Enter mantém): ")
    if tels: campos["telefone"] = tels
    n = usuario.atualizar(cpf, campos)
    resultado(n, f"{n} usuário atualizado.", "Nenhum usuário com esse CPF.")


def u_deletar():
    n = usuario.deletar(ask("CPF do usuário: ", int, True))
    resultado(n, f"{n} usuário removido.", "Nenhum usuário com esse CPF.")


# ---------- professor ----------
def p_inserir():
    print("Formação: Graduação, Especialização, Mestrado, Doutorado | Jornada: 20h, 40h, DE")
    n = professor.inserir(ask("Matrícula (até 7 caracteres): ", obrigatorio=True),
                          ask("CPF do usuário (opcional): ", int),
                          ask("Departamento (ex.: DCOMP): "), ask("Formação: "),
                          ask("Data de admissão (AAAA-MM-DD): "), ask("Jornada: "),
                          ask("Salário: ", float))
    print(f"OK: {n} professor inserido.")


def p_atualizar():
    mat = ask("Matrícula do professor: ", obrigatorio=True)
    campos = coletar([("cpf", "Novo CPF", int), ("departamento", "Novo departamento", str),
                      ("formacao", "Nova formação", str), ("data_admissao", "Nova data de admissão", str),
                      ("tipo_jornada_trabalho", "Nova jornada (20h/40h/DE)", str),
                      ("salario", "Novo salário", float)])
    n = professor.atualizar(mat, campos)
    resultado(n, f"{n} professor atualizado.", "Nenhum professor com essa matrícula.")


def p_deletar():
    n = professor.deletar(ask("Matrícula do professor: ", obrigatorio=True))
    resultado(n, f"{n} professor removido.", "Nenhum professor com essa matrícula.")


# ---------- turma ----------
def t_inserir():
    id_nova = turma.inserir(ask("Código da disciplina (ex.: COMP0123): ", obrigatorio=True),
                            ask("Número da turma: ", int, True),
                            ask("Ano: ", int, True), ask("Semestre (1 ou 2): ", int, True))
    print(f"OK: turma inserida com id_turma = {id_nova}.")


def t_atualizar():
    id_t = ask("id_turma: ", int, True)
    campos = coletar([("cod_disc", "Nova disciplina", str), ("numero", "Novo número", int),
                      ("ano", "Novo ano", int), ("semestre", "Novo semestre", int)])
    n = turma.atualizar(id_t, campos)
    resultado(n, f"{n} turma atualizada.", "Nenhuma turma com esse id.")


def t_deletar():
    print("Atenção: apagar a turma também apaga seus registros em leciona e cursa (CASCADE).")
    n = turma.deletar(ask("id_turma: ", int, True))
    resultado(n, f"{n} turma removida.", "Nenhuma turma com esse id.")


# ---------- leciona ----------
def l_inserir():
    n = leciona.inserir(ask("id_turma: ", int, True), ask("Matrícula do professor: ", obrigatorio=True))
    print(f"OK: {n} vínculo inserido.")


def l_trocar():
    n = leciona.trocar_professor(ask("id_turma: ", int, True),
                                 ask("Matrícula atual: ", obrigatorio=True),
                                 ask("Nova matrícula: ", obrigatorio=True))
    resultado(n, f"{n} vínculo atualizado.", "Vínculo não encontrado.")


def l_deletar():
    n = leciona.deletar(ask("id_turma: ", int, True), ask("Matrícula do professor: ", obrigatorio=True))
    resultado(n, f"{n} vínculo removido.", "Vínculo não encontrado.")


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
