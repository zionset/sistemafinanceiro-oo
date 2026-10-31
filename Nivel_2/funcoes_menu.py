from Nivel_1.classes import MetaInvestimento, CalculadoraInvestimento


def pausar():
    input("\nPressione Enter para continuar...")


# ----- Usuários -----
def cadastrar_usuario(sistema):
    print("\n--- CADASTRO DE USUÁRIO ---")
    login = input("Login: ").strip()
    senha = input("Senha: ")
    nome = input("Nome (opcional): ").strip()
    if sistema.cadastrar_usuario(login, senha, nome):
        print("Usuário cadastrado com sucesso!")
    else:
        print("Erro: login vazio ou já existe!")


def fazer_login(sistema):
    print("\n--- LOGIN ---")
    login = input("Login: ").strip()
    senha = input("Senha: ")
    usuario = sistema.autenticar(login, senha)
    if usuario:
        print(f"Bem-vindo(a), {usuario.nome}!")
    else:
        print("Login ou senha incorretos.")
    return usuario


def listar_usuarios(sistema):
    print("\n--- USUÁRIOS ---")
    for u in sistema.usuarios:
        print(u.visualizar_usuario())


def excluir_conta(sistema, usuario):
    if input("Excluir sua conta e todos os seus dados? (s/n): ").lower() == "s":
        sistema.remover_usuario(usuario.login)
        print("Conta excluída.")
        return True
    return False


# ----- Transações -----
def registrar_receita(sistema, usuario):
    print("\n--- NOVA RECEITA ---")
    descricao = input("Descrição: ")
    valor = float(input("Valor: R$ ").replace(",", "."))
    data = input("Data (dd/mm/aaaa): ")
    categoria = input("Categoria: ")
    receita = sistema.registrar_receita(usuario, descricao, valor, data, categoria)
    print("Registrada:", receita.visualizar_transacao())


def registrar_despesa(sistema, usuario):
    print("\n--- NOVA DESPESA ---")
    descricao = input("Descrição: ")
    valor = float(input("Valor: R$ ").replace(",", "."))
    data = input("Data (dd/mm/aaaa): ")
    categoria = input("Categoria: ")
    pagamento = input("Forma de pagamento: ") or "Dinheiro"
    despesa = sistema.registrar_despesa(usuario, descricao, valor, data, categoria, pagamento)
    print("Registrada:", despesa.visualizar_transacao())


def listar_transacoes(sistema, usuario):
    print("\n--- EXTRATO ---")
    transacoes = sistema.listar_transacoes(usuario)
    if not transacoes:
        print("Nenhuma transação registrada.")
    for t in transacoes:
        print(t.visualizar_transacao())
    print(f"\nReceitas: R${sistema.total_receitas(usuario):.2f}")
    print(f"Despesas: R${sistema.total_despesas(usuario):.2f}")
    print(f"Saldo:    R${sistema.calcular_saldo(usuario):.2f}")


def buscar_transacao_do_usuario(sistema, usuario):
    t = sistema.buscar_transacao(int(input("ID da transação: ")))
    if t and t.usuario is usuario:
        return t
    print("Transação não encontrada.")
    return None


def editar_transacao(sistema, usuario):
    print("\n--- EDITAR TRANSAÇÃO (Enter mantém o valor atual) ---")
    t = buscar_transacao_do_usuario(sistema, usuario)
    if t:
        descricao = input(f"Descrição ({t.descricao}): ") or t.descricao
        valor = input(f"Valor ({t.valor:.2f}): ").replace(",", ".")
        data = input(f"Data ({t.data}): ") or t.data
        t.atualizar(descricao, float(valor) if valor else t.valor, data)
        print("Atualizada:", t.visualizar_transacao())


def excluir_transacao(sistema, usuario):
    print("\n--- EXCLUIR TRANSAÇÃO ---")
    t = buscar_transacao_do_usuario(sistema, usuario)
    if t:
        sistema.remover_transacao(t.id)
        print("Transação removida.")


# ----- Metas -----
def criar_meta(sistema, usuario):
    print("\n--- NOVA META ---")
    titulo = input("Título: ")
    valor_alvo = float(input("Valor alvo: R$ ").replace(",", "."))
    prazo = int(input("Prazo (meses): "))
    taxa = float(input("Juros ao ano (%): ").replace(",", "."))
    meta = sistema.criar_meta(usuario, titulo, valor_alvo, prazo, taxa)
    print("Meta criada:", meta.visualizar_meta())


def simular_meta(usuario):
    print("\n--- SIMULAR APORTE ---")
    valor_alvo = float(input("Valor alvo: R$ ").replace(",", "."))
    prazo = int(input("Prazo (meses): "))
    taxa = float(input("Juros ao ano (%): ").replace(",", "."))
    meta = MetaInvestimento(0, "Simulação", valor_alvo, prazo, taxa, usuario)
    aporte = CalculadoraInvestimento.calcular_aporte_mensal(meta)
    print(f"Aporte mensal necessário: R${aporte:.2f}")


def listar_metas(sistema, usuario):
    print("\n--- MINHAS METAS ---")
    metas = sistema.listar_metas(usuario)
    if not metas:
        print("Nenhuma meta cadastrada.")
    for m in metas:
        print(m.visualizar_meta())


def excluir_meta(sistema, usuario):
    print("\n--- EXCLUIR META ---")
    meta = sistema.buscar_meta(int(input("ID da meta: ")))
    if meta and meta.usuario is usuario:
        sistema.remover_meta(meta.id)
        print("Meta removida.")
    else:
        print("Meta não encontrada.")
