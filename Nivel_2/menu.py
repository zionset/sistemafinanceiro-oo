from package import SistemaFinanceiro
from Nivel_2.funcoes_menu import (
    pausar, cadastrar_usuario, fazer_login, listar_usuarios, excluir_conta,
    registrar_receita, registrar_despesa, listar_transacoes, editar_transacao, excluir_transacao,
    criar_meta, simular_meta, listar_metas, excluir_meta,
)


def nao_salvar(sistema):
    pass  # no Nível 2 os dados ficam só na memória


def exibir_menu_usuario(sistema, usuario):
    print(f"\n===== {usuario.nome} | Saldo: R${sistema.calcular_saldo(usuario):.2f} =====")
    print("1 - Registrar receita")
    print("2 - Registrar despesa")
    print("3 - Ver extrato")
    print("4 - Editar transação")
    print("5 - Excluir transação")
    print("6 - Criar meta")
    print("7 - Simular aporte")
    print("8 - Ver metas")
    print("9 - Excluir meta")
    print("10 - Excluir minha conta")
    print("0 - Sair")


def menu_usuario(sistema, usuario, salvar):
    while True:
        exibir_menu_usuario(sistema, usuario)
        opcao = input("Escolha uma opção: ")
        try:
            match opcao:
                case "1":
                    registrar_receita(sistema, usuario)
                case "2":
                    registrar_despesa(sistema, usuario)
                case "3":
                    listar_transacoes(sistema, usuario)
                case "4":
                    editar_transacao(sistema, usuario)
                case "5":
                    excluir_transacao(sistema, usuario)
                case "6":
                    criar_meta(sistema, usuario)
                case "7":
                    simular_meta(usuario)
                case "8":
                    listar_metas(sistema, usuario)
                case "9":
                    excluir_meta(sistema, usuario)
                case "10":
                    if excluir_conta(sistema, usuario):
                        salvar(sistema)
                        return
                case "0":
                    return
                case _:
                    print("Opção inválida!")
        except ValueError as erro:
            print("Erro: valor inválido!", erro)
        salvar(sistema)
        pausar()


def rodar_sistema(sistema=None, salvar=nao_salvar):
    if sistema is None:
        sistema = SistemaFinanceiro()
    while True:
        print("\n===== SISTEMA DE GESTÃO FINANCEIRA =====")
        print("1 - Entrar")
        print("2 - Cadastrar usuário")
        print("3 - Listar usuários")
        print("0 - Encerrar")
        opcao = input("Escolha uma opção: ")
        match opcao:
            case "1":
                usuario = fazer_login(sistema)
                if usuario:
                    menu_usuario(sistema, usuario, salvar)
            case "2":
                cadastrar_usuario(sistema)
                salvar(sistema)
            case "3":
                listar_usuarios(sistema)
            case "0":
                print("Saindo do sistema...")
                break
            case _:
                print("Opção inválida!")


if __name__ == "__main__":
    rodar_sistema()
