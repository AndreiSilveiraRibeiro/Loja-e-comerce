import pandas as pd
import numpy as np

tabela_clientes = pd.read_csv("tbl_clientes_sujo.csv")
tabela_produtos = pd.read_csv("tbl_produtos_sujo.csv")
tabela_vendas = pd.read_csv("tbl_vendas_sujo.csv")

print(tabela_clientes)