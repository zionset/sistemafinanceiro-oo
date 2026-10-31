"""Demonstração do Nível 1: mostra cada relação de POO funcionando."""
from classes import SistemaFinanceiro, Transacao

sistema = SistemaFinanceiro()

# ---------- COMPOSIÇÃO: o sistema cria os usuários ----------
print("=== 1. Cadastro e login (Composição) ===")
zion = sistema.cadastrar_usuario("zion", "123456", "Zion")
maria = sistema.cadastrar_usuario("maria", "senha789", "Maria")
print(zion.visualizar_usuario())
print(maria.visualizar_usuario())
print("Cadastrar 'zion' de novo:", sistema.cadastrar_usuario("zion", "outra"))  # None
print("Login com senha certa:", sistema.autenticar("zion", "123456") is zion)
print("Login com senha errada:", sistema.autenticar("zion", "000"))

# ---------- ASSOCIAÇÃO: transações ligadas a usuário e categoria ----------
print("\n=== 2. Receitas e despesas (Associação + Herança) ===")
sistema.registrar_receita(zion, "Salário", 5000.0, "10/10/2026", "Trabalho")
sistema.registrar_receita(zion, "Freelance", 1200.0, "15/10/2026", "Trabalho")
aluguel = sistema.registrar_despesa(zion, "Aluguel", 1800.0, "12/10/2026", "Moradia", "Pix")
sistema.registrar_despesa(zion, "Supermercado", 650.0, "14/10/2026", "Alimentação", "Cartão Débito")
sistema.registrar_receita(maria, "Bolsa", 800.0, "05/10/2026", "Estudos")
print(f"{len(sistema.transacoes)} transações registradas.")
print(f"O aluguel pertence a: {aluguel.usuario.nome} | categoria: {aluguel.categoria}")
print("Categorias criadas pelo sistema:", ", ".join(str(c) for c in sistema.categorias))

# ---------- POLIMORFISMO: mesma chamada, comportamentos diferentes ----------
print("\n=== 3. Polimorfismo ===")
for t in sistema.listar_transacoes(zion):
    print(t.visualizar_transacao())

print(f"\nReceitas do Zion: R${sistema.total_receitas(zion):.2f}")
print(f"Despesas do Zion: R${sistema.total_despesas(zion):.2f}")
print(f"Saldo do Zion:    R${sistema.calcular_saldo(zion):.2f}")
print(f"Saldo da Maria:   R${sistema.calcular_saldo(maria):.2f}")

# ---------- CLASSE ABSTRATA ----------
print("\n=== 4. Transacao é abstrata ===")
try:
    Transacao(99, "Teste", 10, "01/01/2026", sistema.obter_categoria("X"), zion)
except TypeError as erro:
    print("Não é possível instanciar Transacao:", erro)

# ---------- DEPENDÊNCIA: Calculadora usa a Meta como parâmetro ----------
print("\n=== 5. Meta de investimento (Dependência) ===")
meta = sistema.criar_meta(zion, "Reserva de emergência", 30000.0, 24, 10.5)
print(meta.visualizar_meta())

# ---------- REMOÇÕES ----------
print("\n=== 6. Remoções ===")
sistema.remover_transacao(aluguel.id)
print(f"Saldo do Zion sem o aluguel: R${sistema.calcular_saldo(zion):.2f}")

sistema.remover_usuario("zion")
print("Usuário zion removido. Transações restantes:", len(sistema.transacoes),
      "| Metas restantes:", len(sistema.metas))
