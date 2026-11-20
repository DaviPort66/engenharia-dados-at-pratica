from relacional import usuario


def pedir_lista(msg):
    return [x.strip() for x in input(msg).split(",") if x.strip()]


def pedir_cpf():
    txt = input("CPF (só números): ").strip()
    if not txt.isdigit():
        raise ValueError("CPF deve conter apenas números.")
    return int(txt)


def mostrar(linhas):
    if not linhas:
        print("Nenhum registro encontrado.")
    for l in linhas:
        print(l)


def menu_usuario():
    while True:
        print("\n--- USUÁRIO ---\n1) Inserir\n2) Listar\n3) Buscar por CPF\n4) Atualizar\n5) Deletar\n0) Voltar")
        op = input("Opção: ").strip()
        try:
            if op == "1":
                cpf = pedir_cpf()
                nome = input("Nome: ").strip()
                nasc = input("Data de nascimento (AAAA-MM-DD, opcional): ").strip()
                emails = pedir_lista("E-mails (separados por vírgula): ")
                tels = pedir_lista("Telefones (separados por vírgula): ")
                login = input("Login: ").strip()
                senha = input("Senha: ").strip()
                n = usuario.inserir(cpf, nome, nasc, emails, tels, login, senha)
                print(f"OK: {n} usuário inserido.")
            elif op == "2":
                mostrar(usuario.listar())
            elif op == "3":
                mostrar(usuario.buscar(pedir_cpf()))
            elif op == "4":
                cpf = pedir_cpf()
                campos = {}
                nome = input("Novo nome (Enter mantém): ").strip()
                if nome: campos["nome"] = nome
                nasc = input("Nova data de nascimento (Enter mantém): ").strip()
                if nasc: campos["data_nascimento"] = nasc
                emails = pedir_lista("Novos e-mails (Enter mantém): ")
                if emails: campos["email"] = emails
                tels = pedir_lista("Novos telefones (Enter mantém): ")
                if tels: campos["telefone"] = tels
                login = input("Novo login (Enter mantém): ").strip()
                if login: campos["login"] = login
                senha = input("Nova senha (Enter mantém): ").strip()
                if senha: campos["senha"] = senha
                n = usuario.atualizar(cpf, campos)
                print(f"OK: {n} usuário atualizado." if n else "Nenhum usuário com esse CPF.")
            elif op == "5":
                n = usuario.deletar(pedir_cpf())
                print(f"OK: {n} usuário removido." if n else "Nenhum usuário com esse CPF.")
            elif op == "0":
                return
            else:
                print("Opção inválida.")
        except ValueError as e:
            print(f"Erro: {e}")


def main():
    while True:
        print("\n=== CRUD UNIVERSIDADE ===\n1) Usuário\n0) Sair")
        op = input("Opção: ").strip()
        if op == "1":
            menu_usuario()
        elif op == "0":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
