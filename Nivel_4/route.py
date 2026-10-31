from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from Nivel_1.classes import MetaInvestimento, CalculadoraInvestimento
from Nivel_3.dados import carregar_dados, salvar_dados

app = Flask(__name__)
app.secret_key = "orientacao-a-objetos"

sistema = carregar_dados()


def usuario_logado():
    return sistema.buscar_usuario(session.get("usuario", ""))


# Filtros usados nos templates
@app.template_filter("moeda")
def moeda(valor):
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


@app.template_filter("data_iso")
def data_iso(data):
    return datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")


def data_do_formulario():
    # o campo de data do HTML envia aaaa-mm-dd; o sistema guarda dd/mm/aaaa
    return datetime.strptime(request.form["data"], "%Y-%m-%d").strftime("%d/%m/%Y")


# ---------- Usuários ----------
@app.route("/")
def inicio():
    return redirect(url_for("painel"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = sistema.autenticar(request.form["login"], request.form["senha"])
        if usuario:
            session["usuario"] = usuario.login
            return redirect(url_for("painel"))
        flash("Login ou senha incorretos.", "erro")
    return render_template("login.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        if sistema.cadastrar_usuario(request.form["login"], request.form["senha"], request.form["nome"]):
            salvar_dados(sistema)
            flash("Conta criada! Agora é só entrar.", "sucesso")
            return redirect(url_for("login"))
        flash("Esse login já existe.", "erro")
    return render_template("cadastro.html")


@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))


@app.route("/conta/excluir", methods=["POST"])
def excluir_conta():
    usuario = usuario_logado()
    if usuario:
        sistema.remover_usuario(usuario.login)
        salvar_dados(sistema)
        session.pop("usuario", None)
        flash("Sua conta foi excluída.", "aviso")
    return redirect(url_for("login"))


# ---------- Painel ----------
@app.route("/painel")
def painel():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("login"))
    transacoes = sistema.listar_transacoes(usuario)
    return render_template("painel.html", usuario=usuario,
                           saldo=sistema.calcular_saldo(usuario),
                           receitas=sistema.total_receitas(usuario),
                           despesas=sistema.total_despesas(usuario),
                           ultimas=transacoes[::-1][:5],
                           metas=sistema.listar_metas(usuario))


# ---------- Transações ----------
@app.route("/transacoes", methods=["GET", "POST"])
def transacoes():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            descricao = request.form["descricao"]
            valor = float(request.form["valor"])
            categoria = request.form["categoria"]
            if request.form["tipo"] == "Receita":
                sistema.registrar_receita(usuario, descricao, valor, data_do_formulario(), categoria)
            else:
                sistema.registrar_despesa(usuario, descricao, valor, data_do_formulario(), categoria,
                                          request.form["forma_pagamento"])
            salvar_dados(sistema)
            flash("Transação registrada.", "sucesso")
        except ValueError as erro:
            flash(f"Erro: {erro}", "erro")
        return redirect(url_for("transacoes"))

    filtro = request.args.get("tipo", "")
    lista = [t for t in sistema.listar_transacoes(usuario) if filtro == "" or t.tipo == filtro]
    return render_template("transacoes.html", usuario=usuario, transacoes=lista[::-1], filtro=filtro,
                           hoje=datetime.now().strftime("%Y-%m-%d"))


@app.route("/transacoes/<int:id_transacao>/editar", methods=["GET", "POST"])
def editar_transacao(id_transacao):
    usuario = usuario_logado()
    t = sistema.buscar_transacao(id_transacao)
    if not usuario or not t or t.usuario is not usuario:
        return redirect(url_for("transacoes"))

    if request.method == "POST":
        try:
            t.atualizar(request.form["descricao"], float(request.form["valor"]), data_do_formulario())
            salvar_dados(sistema)
            flash("Transação atualizada.", "sucesso")
            return redirect(url_for("transacoes"))
        except ValueError as erro:
            flash(f"Erro: {erro}", "erro")
    return render_template("editar_transacao.html", usuario=usuario, t=t)


@app.route("/transacoes/<int:id_transacao>/excluir", methods=["POST"])
def excluir_transacao(id_transacao):
    usuario = usuario_logado()
    t = sistema.buscar_transacao(id_transacao)
    if usuario and t and t.usuario is usuario:
        sistema.remover_transacao(id_transacao)
        salvar_dados(sistema)
        flash("Transação excluída.", "sucesso")
    return redirect(url_for("transacoes"))


# ---------- Metas ----------
@app.route("/metas", methods=["GET", "POST"])
def metas():
    usuario = usuario_logado()
    if not usuario:
        return redirect(url_for("login"))

    simulacao = None
    if request.method == "POST":
        titulo = request.form["titulo"] or "Simulação"
        valor_alvo = float(request.form["valor_alvo"])
        prazo = int(request.form["prazo_meses"])
        taxa = float(request.form["taxa_juros_anual"])
        if request.form["acao"] == "simular":
            simulacao = MetaInvestimento(0, titulo, valor_alvo, prazo, taxa, usuario)
            CalculadoraInvestimento.calcular_aporte_mensal(simulacao)
        else:
            sistema.criar_meta(usuario, titulo, valor_alvo, prazo, taxa)
            salvar_dados(sistema)
            flash("Meta criada.", "sucesso")
            return redirect(url_for("metas"))

    return render_template("metas.html", usuario=usuario, metas=sistema.listar_metas(usuario),
                           simulacao=simulacao)


@app.route("/metas/<int:id_meta>/excluir", methods=["POST"])
def excluir_meta(id_meta):
    usuario = usuario_logado()
    meta = sistema.buscar_meta(id_meta)
    if usuario and meta and meta.usuario is usuario:
        sistema.remover_meta(id_meta)
        salvar_dados(sistema)
        flash("Meta excluída.", "sucesso")
    return redirect(url_for("metas"))


if __name__ == "__main__":
    app.run(debug=True)
