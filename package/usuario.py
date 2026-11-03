class Usuario:
    def __init__(self, login, senha, nome=""):
        self.login = login
        self.senha = senha
        self.nome = nome or login.title()

    def verificar_senha(self, senha_digitada):
        return self.senha == senha_digitada

    def visualizar_usuario(self):
        return f"Usuário: {self.nome} (Login: {self.login})"
