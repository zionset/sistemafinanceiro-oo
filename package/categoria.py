class Categoria:
    def __init__(self, nome, tipo="Geral"):
        self.nome = nome.strip().title()
        self.tipo = tipo

    def __str__(self):
        return self.nome
