import pandas as pd
import numpy as np

tabela_clientes = pd.read_csv("tbl_clientes_sujo.csv")
tabela_produtos = pd.read_csv("tbl_produtos_sujo.csv")
tabela_vendas = pd.read_csv("tbl_vendas_sujo.csv")

print(tabela_clientes)
print(tabela_clientes.shape)
tabela_clientes.info()
print(tabela_clientes.isnull().sum())

print(tabela_clientes['nome_cliente'])

tabela_clientes['nome_cliente'] = tabela_clientes['nome_cliente'].str.strip().str.title()

print(tabela_clientes['nome_cliente'])
print(tabela_clientes['nome_cliente'].unique())

print(tabela_clientes['estado'])

tabela_clientes['estado'] = tabela_clientes['estado'].str.strip()

print(tabela_clientes['estado'])
print(tabela_clientes['estado'].unique())

estado_sigla = {

    'Rio de Janeiro': 'RJ',
    'S.Paulo': 'SP',
    'sp': 'SP',
    'São Paulo': 'SP',
     'Minas Gerais': 'MG'

}

ddd_errado = ~tabela_clientes['estado'].str.contains(r'^[a-zA-Z]{2}$', regex=True, na=False)
tabela_clientes.loc[ddd_errado, 'estado'] = tabela_clientes.loc[ddd_errado, 'estado'].map(estado_sigla)
tabela_clientes['estado'] = tabela_clientes['estado'].str.upper()

print(tabela_clientes[tabela_clientes['estado'].isna()])
print(tabela_clientes['estado'])

print(tabela_clientes['email'])

print(tabela_clientes)
print(tabela_clientes.shape)
tabela_clientes.info()
print(tabela_clientes.isnull().sum())

#parte dois

print(tabela_produtos)
print(tabela_produtos.shape)
tabela_produtos.info()
print(tabela_produtos.isnull().sum())

print(tabela_produtos['id_produto'])

tabela_produtos['nome_produto'] = tabela_produtos['nome_produto'].str.strip().str.title()
tabela_produtos['categoria'] = tabela_produtos['categoria'].str.strip().str.title()

tabela_produtos['categoria'] = tabela_produtos['categoria'].replace('???', 'Moveis')

print(tabela_produtos['nome_produto'].unique())
print(tabela_produtos['categoria'].unique())

analise = {

    'Romance Pro': 'Livros',
    'Fone Pro': 'Eletrônicos',
    'Arroz': 'Alimentos',
    'Camiseta': 'Vestuário',
    'Fone Premium': 'Eletrônicos',
    'Calça Jeans': 'Vestuário',
    'Notebook': 'Eletrônicos',
    'Feijão': 'Alimentos',
    'Carregador': 'Eletrônicos',
    'Fone': 'Eletrônicos',
    'Mesa': 'Moveis',
    'Camiseta Premium': 'Vestuário',
    'Romance': 'Livros',
    'Cadeiranan': 'Livros',
    'Ficção Científica': 'Livros',
    'Smartphone': 'Eletrônicos',
    'Ficção Científica Pro': 'Livros',
    'Notebook Pro': 'Eletrônicos',
    'Cadeira': 'Moveis',
    'Cadeira Pro': 'Moveis',
    'Camiseta Pro': 'Vestuário',
    'Feijão Premium': 'Alimentos',
    'Mesa Pro': 'Moveis',
    'Carregador Pro': 'Eletrônicos',
    'Romance Premium': 'Livros'

}

tabela_produtos['categoria'] = tabela_produtos['nome_produto'].map(analise)

print(tabela_produtos)
print(tabela_produtos['categoria'].isnull().sum())

print(tabela_produtos['preco_custo'])

tabela_produtos['preco_custo'] = tabela_produtos['preco_custo'].str.replace('R$', '', regex=False)
tabela_produtos['preco_custo'] = tabela_produtos['preco_custo'].str.replace(',', '.', regex=False)
tabela_produtos['preco_custo'] = tabela_produtos['preco_custo'].astype(float)

print(tabela_produtos['preco_custo'])

print(tabela_produtos[tabela_produtos['preco_custo'] < 0])

print(tabela_produtos)
print(tabela_produtos.shape)
tabela_produtos.info()
print(tabela_produtos.isnull().sum())
print(tabela_produtos.describe())

#parte três

print(tabela_vendas)
print(tabela_vendas.shape)
tabela_vendas.info()
print(tabela_vendas.isnull().sum())

print(tabela_vendas['data_venda'])

# 1. Convertemos a coluna para o tipo Data real do Pandas (informando o formato dia/mês/ano)
tabela_vendas['data_venda'] = pd.to_datetime(tabela_vendas['data_venda'], format='%d/%m/%Y', errors='coerce')

# 2. Definimos a nossa data limite como um objeto de data real
data_limite = pd.to_datetime('2026-06-16')

# 3. Agora o print funciona perfeitamente por ordem cronológica!
print(f"Datas erradas: \n{tabela_vendas[tabela_vendas['data_venda'] > data_limite]}")

tabela_vendas['data_venda'] = np.where(tabela_vendas['data_venda'] > data_limite, pd.NA, tabela_vendas['data_venda'])

print(tabela_vendas['data_venda'])

print(tabela_vendas['quantidade'])
print(tabela_vendas[tabela_vendas['quantidade'] < 0])

mediana = tabela_vendas.loc[tabela_vendas['quantidade'] >= 0, 'quantidade'].median()

tabela_vendas['quantidade'] = np.where(tabela_vendas['quantidade'] < -5, mediana, tabela_vendas['quantidade'].abs())

print(tabela_vendas[tabela_vendas['quantidade'] < 0])

print(tabela_vendas['preco_unitario'])
print(tabela_vendas[tabela_vendas['preco_unitario'] < 0])

print(tabela_vendas['desconto_percent'])
print(tabela_vendas[tabela_vendas['desconto_percent'].isna()])

tabela_vendas['desconto_percent'] = tabela_vendas['desconto_percent'].fillna(0)

print(tabela_vendas['desconto_percent'])
print(tabela_vendas[tabela_vendas['desconto_percent'].isna()])