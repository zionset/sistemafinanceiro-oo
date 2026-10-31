from abc import ABC, abstractmethod


class Usuario:
    def __init__(self, login, senha, nome=""):
        self.login = login
        self.senha = senha
        self.nome = nome or login.title()

    def verificar_senha(self, senha_digitada):
        return self.senha == senha_digitada

    def visualizar_usuario(self):
        return f"Usuário: {self.nome} (Login: {self.login})"


class Categoria:
    def __init__(self, nome, tipo="Geral"):
        self.nome = nome.strip().title()
        self.tipo = tipo

    def __str__(self):
        return self.nome


# Classe abstrata: não pode ser instanciada, só Receita e Despesa
class Transacao(ABC):
    def __init__(self, id_transacao, descricao, valor, data, categoria, usuario):
        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero.")
        self.id = id_transacao
        self.descricao = descricao
        self.valor = float(valor)
        self.data = data
        self.categoria = categoria  # associação
        self.usuario = usuario      # associação

    @abstractmethod
    def aplicar_saldo(self, saldo_atual):
        pass

    def atualizar(self, descricao, valor, data):
        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero.")
        self.descricao = descricao
        self.valor = float(valor)
        self.data = data

    def visualizar_transacao(self):
        return f"[{self.data}] #{self.id} {self.descricao} - R${self.valor:.2f} ({self.categoria})"


# Herança + polimorfismo: cada filha aplica o saldo do seu jeito
class Receita(Transacao):
    def __init__(self, id_transacao, descricao, valor, data, categoria, usuario):
        super().__init__(id_transacao, descricao, valor, data, categoria, usuario)
        self.tipo = "Receita"

    def aplicar_saldo(self, saldo_atual):
        return saldo_atual + self.valor

    def visualizar_transacao(self):
        return f"[RECEITA] {self.data} | #{self.id} {self.descricao} | +R${self.valor:.2f} | {self.categoria}"


class Despesa(Transacao):
    def __init__(self, id_transacao, descricao, valor, data, categoria, usuario, forma_pagamento="Dinheiro"):
        super().__init__(id_transacao, descricao, valor, data, categoria, usuario)
        self.tipo = "Despesa"
        self.forma_pagamento = forma_pagamento.title()

    def aplicar_saldo(self, saldo_atual):
        return saldo_atual - self.valor

    def visualizar_transacao(self):
        return (f"[DESPESA] {self.data} | #{self.id} {self.descricao} | -R${self.valor:.2f} | "
                f"{self.categoria} | {self.forma_pagamento}")


class MetaInvestimento:
    def __init__(self, id_meta, titulo, valor_alvo, prazo_meses, taxa_juros_anual, usuario):
        self.id = id_meta
        self.titulo = titulo
        self.valor_alvo = valor_alvo
        self.prazo_meses = prazo_meses
        self.taxa_juros_anual = taxa_juros_anual
        self.usuario = usuario  # associação
        self.aporte_mensal = 0.0

    def visualizar_meta(self):
        return (f"Meta #{self.id}: {self.titulo} - R${self.valor_alvo:.2f} em {self.prazo_meses} meses "
                f"({self.taxa_juros_anual}% ao ano) | Aporte: R${self.aporte_mensal:.2f}/mês")


# Dependência: só recebe a meta como parâmetro, não guarda nada
class CalculadoraInvestimento:
    @staticmethod
    def calcular_aporte_mensal(meta):
        # Juros compostos: aporte = valor_alvo * i / ((1 + i)^n - 1)
        taxa_mensal = meta.taxa_juros_anual / 100 / 12
        n = meta.prazo_meses
        if taxa_mensal == 0:
            aporte = meta.valor_alvo / n
        else:
            aporte = meta.valor_alvo * taxa_mensal / ((1 + taxa_mensal) ** n - 1)
        meta.aporte_mensal = round(aporte, 2)
        return meta.aporte_mensal


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
