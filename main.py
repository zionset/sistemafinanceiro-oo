"""Ponto de entrada do sistema no terminal (Nível 2 + Nível 3).

O menu do Nível 2 roda com os dados carregados do database.json e salva
automaticamente a cada alteração.
    python main.py
"""
from Nivel_2.menu import rodar_sistema
from Nivel_3.dados import carregar_dados, salvar_dados

if __name__ == "__main__":
    rodar_sistema(carregar_dados(), salvar_dados)
