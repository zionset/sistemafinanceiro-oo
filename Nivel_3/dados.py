import json
import os
from Nivel_1.classes import SistemaFinanceiro, Usuario, Categoria, Receita, Despesa, MetaInvestimento, CalculadoraInvestimento

banco_dados = "database.json"


def salvar_dados(sistema, arquivo=banco_dados):
    dados = {
        "usuarios": [
            {"login": u.login, "senha": u.senha, "nome": u.nome} for u in sistema.usuarios
        ],
        "categorias": [
            {"nome": c.nome, "tipo": c.tipo} for c in sistema.categorias
        ],
        "transacoes": [
            {"id": t.id, "tipo": t.tipo, "descricao": t.descricao, "valor": t.valor, "data": t.data,
             "categoria": t.categoria.nome, "usuario": t.usuario.login,
             "forma_pagamento": t.forma_pagamento if t.tipo == "Despesa" else None}
            for t in sistema.transacoes
        ],
        "metas": [
            {"id": m.id, "titulo": m.titulo, "valor_alvo": m.valor_alvo, "prazo_meses": m.prazo_meses,
             "taxa_juros_anual": m.taxa_juros_anual, "usuario": m.usuario.login}
            for m in sistema.metas
        ],
    }
    try:
        # encoding utf-8 para não dar problema com acentos
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except Exception as erro:
        print(f"Erro ao salvar dados: {erro}")


def carregar_dados(arquivo=banco_dados):
    sistema = SistemaFinanceiro()
    if not os.path.exists(arquivo):
        return sistema

    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)

        for u in dados.get("usuarios", []):
            sistema.usuarios.append(Usuario(u["login"], u["senha"], u["nome"]))

        for c in dados.get("categorias", []):
            sistema.categorias.append(Categoria(c["nome"], c["tipo"]))

        for t in dados.get("transacoes", []):
            usuario = sistema.buscar_usuario(t["usuario"])
            categoria = sistema.obter_categoria(t["categoria"], t["tipo"])
            # o campo "tipo" diz se volta como Receita ou Despesa (polimorfismo)
            if t["tipo"] == "Receita":
                transacao = Receita(t["id"], t["descricao"], t["valor"], t["data"], categoria, usuario)
            else:
                transacao = Despesa(t["id"], t["descricao"], t["valor"], t["data"], categoria, usuario,
                                    t["forma_pagamento"])
            sistema.transacoes.append(transacao)

        for m in dados.get("metas", []):
            meta = MetaInvestimento(m["id"], m["titulo"], m["valor_alvo"], m["prazo_meses"],
                                    m["taxa_juros_anual"], sistema.buscar_usuario(m["usuario"]))
            CalculadoraInvestimento.calcular_aporte_mensal(meta)
            sistema.metas.append(meta)
    except Exception as erro:
        print(f"Erro ao carregar dados: {erro}")

    return sistema
