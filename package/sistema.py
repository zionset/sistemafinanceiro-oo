from package.usuario import Usuario
from package.categoria import Categoria
from package.transacao import Receita, Despesa
from package.investimento import MetaInvestimento, CalculadoraInvestimento


# Composição: o sistema cria e é dono dos usuários, categorias, transações e metas
class SistemaFinanceiro:
    def __init__(self):
        self.usuarios = []
        self.categorias = []
        self.transacoes = []
        self.metas = []

    # ----- Usuários -----
    def cadastrar_usuario(self, login, senha, nome=""):
        if not login or not senha or self.buscar_usuario(login):
            return None
        usuario = Usuario(login, senha, nome)
        self.usuarios.append(usuario)
        return usuario

    def buscar_usuario(self, login):
        for u in self.usuarios:
            if u.login == login:
                return u
        return None

    def autenticar(self, login, senha):
        usuario = self.buscar_usuario(login)
        if usuario and usuario.verificar_senha(senha):
            return usuario
        return None

    def remover_usuario(self, login):
        usuario = self.buscar_usuario(login)
        if not usuario:
            return False
        self.usuarios.remove(usuario)
        # as partes são apagadas junto com o usuário (composição)
        self.transacoes = [t for t in self.transacoes if t.usuario is not usuario]
        self.metas = [m for m in self.metas if m.usuario is not usuario]
        return True

    # ----- Categorias -----
    def obter_categoria(self, nome, tipo="Geral"):
        for c in self.categorias:
            if c.nome == nome.strip().title():
                return c
        categoria = Categoria(nome, tipo)
        self.categorias.append(categoria)
        return categoria

    # ----- Transações -----
    def proximo_id_transacao(self):
        return max([t.id for t in self.transacoes], default=0) + 1

    def registrar_receita(self, usuario, descricao, valor, data, nome_categoria):
        categoria = self.obter_categoria(nome_categoria, "Receita")
        receita = Receita(self.proximo_id_transacao(), descricao, valor, data, categoria, usuario)
        self.transacoes.append(receita)
        return receita

    def registrar_despesa(self, usuario, descricao, valor, data, nome_categoria, forma_pagamento="Dinheiro"):
        categoria = self.obter_categoria(nome_categoria, "Despesa")
        despesa = Despesa(self.proximo_id_transacao(), descricao, valor, data, categoria, usuario, forma_pagamento)
        self.transacoes.append(despesa)
        return despesa

    def buscar_transacao(self, id_transacao):
        for t in self.transacoes:
            if t.id == id_transacao:
                return t
        return None

    def listar_transacoes(self, usuario):
        return [t for t in self.transacoes if t.usuario is usuario]

    def remover_transacao(self, id_transacao):
        t = self.buscar_transacao(id_transacao)
        if t:
            self.transacoes.remove(t)
            return True
        return False

    def calcular_saldo(self, usuario):
        # polimorfismo: não importa se é Receita ou Despesa
        saldo = 0.0
        for t in self.listar_transacoes(usuario):
            saldo = t.aplicar_saldo(saldo)
        return round(saldo, 2)

    def total_receitas(self, usuario):
        return sum(t.valor for t in self.listar_transacoes(usuario) if isinstance(t, Receita))

    def total_despesas(self, usuario):
        return sum(t.valor for t in self.listar_transacoes(usuario) if isinstance(t, Despesa))

    # ----- Metas -----
    def criar_meta(self, usuario, titulo, valor_alvo, prazo_meses, taxa_juros_anual):
        novo_id = max([m.id for m in self.metas], default=0) + 1
        meta = MetaInvestimento(novo_id, titulo, valor_alvo, prazo_meses, taxa_juros_anual, usuario)
        CalculadoraInvestimento.calcular_aporte_mensal(meta)  # dependência
        self.metas.append(meta)
        return meta

    def buscar_meta(self, id_meta):
        for m in self.metas:
            if m.id == id_meta:
                return m
        return None

    def listar_metas(self, usuario):
        return [m for m in self.metas if m.usuario is usuario]

    def remover_meta(self, id_meta):
        meta = self.buscar_meta(id_meta)
        if meta:
            self.metas.remove(meta)
            return True
        return False
