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
