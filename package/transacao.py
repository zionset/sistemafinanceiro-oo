from abc import ABC, abstractmethod


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
