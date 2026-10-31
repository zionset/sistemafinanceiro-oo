import unittest
from classes import Usuario, Categoria, Transacao, Receita, Despesa, MetaInvestimento, CalculadoraInvestimento, SistemaFinanceiro


class TestClasses(unittest.TestCase):

    def setUp(self):
        self.usuario = Usuario("zion", "123")
        self.categoria = Categoria("trabalho")

    def test_senha(self):
        self.assertTrue(self.usuario.verificar_senha("123"))
        self.assertFalse(self.usuario.verificar_senha("errada"))

    def test_transacao_e_abstrata(self):
        with self.assertRaises(TypeError):
            Transacao(1, "x", 10, "01/01/2026", self.categoria, self.usuario)

    def test_heranca_e_polimorfismo(self):
        r = Receita(1, "Salário", 100, "01/01/2026", self.categoria, self.usuario)
        d = Despesa(2, "Luz", 30, "01/01/2026", self.categoria, self.usuario, "pix")
        self.assertIsInstance(r, Transacao)
        self.assertIsInstance(d, Transacao)
        self.assertEqual(r.aplicar_saldo(50), 150)
        self.assertEqual(d.aplicar_saldo(50), 20)
        self.assertEqual(d.forma_pagamento, "Pix")

    def test_valor_invalido(self):
        with self.assertRaises(ValueError):
            Receita(1, "Nada", 0, "01/01/2026", self.categoria, self.usuario)

    def test_atualizar(self):
        d = Despesa(1, "Luz", 50, "01/01/2026", self.categoria, self.usuario)
        d.atualizar("Energia", 80, "02/01/2026")
        self.assertEqual((d.descricao, d.valor, d.data), ("Energia", 80, "02/01/2026"))

    def test_associacao(self):
        r = Receita(1, "Salário", 100, "01/01/2026", self.categoria, self.usuario)
        self.assertIs(r.usuario, self.usuario)
        self.assertEqual(str(r.categoria), "Trabalho")

    def test_calculadora(self):
        meta = MetaInvestimento(1, "Reserva", 30000, 24, 10.5, self.usuario)
        self.assertEqual(CalculadoraInvestimento.calcular_aporte_mensal(meta), 1128.78)
        sem_juros = MetaInvestimento(2, "Viagem", 1200, 12, 0, self.usuario)
        self.assertEqual(CalculadoraInvestimento.calcular_aporte_mensal(sem_juros), 100.0)


class TestSistema(unittest.TestCase):

    def setUp(self):
        self.sistema = SistemaFinanceiro()
        self.zion = self.sistema.cadastrar_usuario("zion", "123", "Zion")
        self.maria = self.sistema.cadastrar_usuario("maria", "456")

    def test_cadastro_e_login(self):
        self.assertEqual(len(self.sistema.usuarios), 2)
        self.assertIsNone(self.sistema.cadastrar_usuario("zion", "outra"))  # repetido
        self.assertIs(self.sistema.autenticar("zion", "123"), self.zion)
        self.assertIsNone(self.sistema.autenticar("zion", "errada"))

    def test_saldo(self):
        self.sistema.registrar_receita(self.zion, "Salário", 5000, "10/10/2026", "Trabalho")
        self.sistema.registrar_despesa(self.zion, "Aluguel", 1500, "12/10/2026", "Moradia")
        self.sistema.registrar_receita(self.maria, "Bolsa", 800, "10/10/2026", "Estudos")
        self.assertEqual(self.sistema.calcular_saldo(self.zion), 3500)
        self.assertEqual(self.sistema.total_receitas(self.zion), 5000)
        self.assertEqual(self.sistema.total_despesas(self.zion), 1500)
        self.assertEqual(self.sistema.calcular_saldo(self.maria), 800)

    def test_categoria_reaproveitada(self):
        r1 = self.sistema.registrar_receita(self.zion, "Salário", 100, "01/01/2026", "Trabalho")
        r2 = self.sistema.registrar_receita(self.zion, "Bônus", 50, "02/01/2026", "trabalho")
        self.assertIs(r1.categoria, r2.categoria)

    def test_remover_transacao(self):
        d = self.sistema.registrar_despesa(self.zion, "Luz", 100, "01/01/2026", "Casa")
        self.assertTrue(self.sistema.remover_transacao(d.id))
        self.assertIsNone(self.sistema.buscar_transacao(d.id))

    def test_metas(self):
        meta = self.sistema.criar_meta(self.zion, "Reserva", 30000, 24, 10.5)
        self.assertEqual(meta.aporte_mensal, 1128.78)
        self.assertIn(meta, self.sistema.listar_metas(self.zion))
        self.assertTrue(self.sistema.remover_meta(meta.id))

    def test_composicao(self):
        self.sistema.registrar_receita(self.zion, "Salário", 100, "01/01/2026", "Trabalho")
        self.sistema.criar_meta(self.zion, "Reserva", 1000, 10, 5)
        self.sistema.remover_usuario("zion")
        self.assertEqual(self.sistema.transacoes, [])
        self.assertEqual(self.sistema.metas, [])


if __name__ == "__main__":
    unittest.main()
