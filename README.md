# 💼 SISTEMA DE GESTÃO FINANCEIRA

Foi desenvolvido um sistema para gestão financeira pessoal, com controle de receitas e despesas e planejamento de metas de investimento.

---

## 🚀 Sobre o projeto

O objetivo do projeto é ajudar a organizar o dinheiro do dia a dia: saber quanto entrou, quanto saiu e quanto é preciso guardar por mês para alcançar uma meta.

---

## Funcionalidades do Sistema

* **Login e usuários:** cada usuário tem sua conta e só vê os próprios dados.
* **Receitas e despesas:** cadastro, consulta, edição e exclusão, com o saldo calculado na hora.
* **Categorias:** cada transação tem uma categoria (Trabalho, Moradia, Alimentação...).
* **Metas de investimento:** calcula o aporte mensal necessário usando juros compostos.

---

## 🏗️ Estrutura e Arquitetura do Projeto

Como este projeto foi desenvolvido para a disciplina de Orientação a Objetos, o código foi estruturado em Níveis:

* **Nível 1 (Modelos/Classes):** a base do projeto, com herança, polimorfismo, composição, associação e dependência. As classes ficam na pasta `package/` e os diagramas UML estão no [DIAGRAMAS.md](DIAGRAMAS.md).

* **Nível 2 (CRUD):** menu no terminal com acesso a todas as funcionalidades.

* **Nível 3 (Persistência):** onde foi implantado o banco de dados JSON (`database.json`).

* **Nível 4 (Interface Web - Flask):** onde o projeto deixou de ser só terminal e ganhou um site.

### Organização das pastas

```
sistemafinanceiro-oo/
├── package/              # módulos com as classes do sistema
│   ├── usuario.py        # Usuario
│   ├── categoria.py      # Categoria
│   ├── transacao.py      # Transacao (abstrata), Receita, Despesa
│   ├── investimento.py   # MetaInvestimento, CalculadoraInvestimento
│   └── sistema.py        # SistemaFinanceiro
├── Nivel_1/              # demonstração e testes das classes
├── Nivel_2/              # menu no terminal (CRUD)
├── Nivel_3/              # persistência em JSON
├── Nivel_4/              # interface web (Flask)
├── img/                  # diagramas UML
└── main.py               # terminal com banco de dados
```

---

## 💻 Como Executar o Projeto

Antes de escolher a forma de rodar, faça o download do projeto clonando este repositório:

```bash
git clone https://github.com/<seu-usuario>/sistemafinanceiro-oo.git
cd sistemafinanceiro-oo
```

### 1. Execução via Web (Flask)
É a versão completa do sistema, com interface gráfica no navegador.
* Instale o Flask: `pip install flask`
* Execute o arquivo de rotas: `python -m Nivel_4.route`
* Acesse no navegador: `http://127.0.0.1:5000`

### 2. Execução via Terminal (com banco de dados)
Roda o CRUD do Nível 2 salvando tudo no banco do Nível 3.
* Execute o arquivo principal: `python main.py`
* Para rodar só o Nível 2, sem banco: `python -m Nivel_2.menu`

### 3. Classes do Nível 1
Para ver a demonstração e rodar os testes (a partir da raiz do projeto):
* Demonstração: `python -m Nivel_1.main`
* Testes: `python -m unittest Nivel_1.test_sistema -v`
