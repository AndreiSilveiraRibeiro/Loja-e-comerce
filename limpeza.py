import pandas as pd
import numpy as np

# Carregamento dos dados brutos
tabela_clientes = pd.read_csv("tbl_clientes_sujo.csv")
tabela_produtos = pd.read_csv("tbl_produtos_sujo.csv")
tabela_vendas = pd.read_csv("tbl_vendas_sujo.csv")

# ==========================================================
# PARTE 1: LIMPEZA DOS CLIENTES (NOME, ESTADO E E-MAILS)
# ==========================================================

print(tabela_clientes)
print(tabela_clientes.shape)
tabela_clientes.info()
print(tabela_clientes.isnull().sum())

# --- TRATAMENTO DOS NOMES DOS CLIENTES ---
print(tabela_clientes['nome_cliente'])
tabela_clientes['nome_cliente'] = tabela_clientes['nome_cliente'].str.strip().str.title()
print(tabela_clientes['nome_cliente'])
print(tabela_clientes['nome_cliente'].unique())

# --- TRATAMENTO DOS ESTADOS E SIGLAS ---
print(tabela_clientes['estado'])
tabela_clientes['estado'] = tabela_clientes['estado'].str.strip()
print(tabela_clientes['estado'])
print(tabela_clientes['estado'].unique())

estado_sigla = {
    'Rio de Janeiro': 'RJ',
    'S.Paulo': 'SP',
    'São Paulo': 'SP',
    'Minas Gerais': 'MG'
}

ddd_errado = ~tabela_clientes['estado'].str.contains(r'^[a-zA-Z]{2}$', regex=True, na=False)
tabela_clientes.loc[ddd_errado, 'estado'] = tabela_clientes.loc[ddd_errado, 'estado'].map(estado_sigla)
tabela_clientes['estado'] = tabela_clientes['estado'].str.upper()

print(tabela_clientes[tabela_clientes['estado'].isna()])
print(tabela_clientes['estado'].unique())
print(tabela_clientes['estado'])

# --- VALIDAÇÃO E LIMPEZA DE E-MAILS (CONTAINS + DROP DUPLICATES) ---
# 1. Primeiro identificamos e invalidamos e-mails sem o '@'
tabela_clientes['email'] = np.where(~tabela_clientes['email'].str.contains("@", na=False), pd.NA, tabela_clientes['email'])

# 2. Depois removemos as linhas duplicadas (mantendo apenas o primeiro registro válido)
print(f"Duplicados antes: {tabela_clientes['email'].duplicated().sum()}")
tabela_clientes = tabela_duplicates = tabela_clientes.drop_duplicates(subset=['email'], keep='first')
print(f"Duplicados depois: {tabela_clientes['email'].duplicated().sum()}")

# --- VALIDAÇÃO FINAL DA TABELA DE CLIENTES ---
print(tabela_clientes)
print(tabela_clientes.shape)
tabela_clientes.info()
print(tabela_clientes.isnull().sum())


# ==========================================================
# PARTE 2: LIMPEZA DOS PRODUTOS (CATEGORIAS E PREÇOS)
# ==========================================================

print(tabela_produtos)
print(tabela_produtos.shape)
tabela_produtos.info()
print(tabela_produtos.isnull().sum())

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


# ==========================================================
# PARTE 3: LIMPEZA DAS VENDAS (DATAS, QUANTIDADES E DESCONTOS)
# ==========================================================

print(tabela_vendas)
print(tabela_vendas.shape)
tabela_vendas.info()
print(tabela_vendas.isnull().sum())

print(tabela_vendas['data_venda'])

tabela_vendas['data_venda_formatada'] = tabela_vendas['data_venda'].replace(r'(\d{4})-(\d{2})-(\d{2})', r'\3/\2/\1', regex=True)
tabela_vendas['data_venda'] = pd.to_datetime(tabela_vendas['data_venda'], format='%Y-%m-%d', errors='coerce', yearfirst=True)

print(tabela_vendas['data_venda_formatada'])
print(f"Anos errados: \n{tabela_vendas[tabela_vendas['data_venda'].dt.year > 2026]}")

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

print(tabela_vendas['frete'])
print(tabela_vendas[tabela_vendas['frete'].isna()])
print(tabela_vendas[tabela_vendas['frete'] < 0])


# ==========================================================
# PARTE 4: CONSOLIDANDO AS BASES (O MERGE DO CHEFE)
# ==========================================================

print(f"Tabela clientes: \n{tabela_clientes}")
print(f"Tabela vendas: \n{tabela_vendas}")
print(f"Tabela produtos: \n{tabela_produtos}")

tabela_primaria = pd.merge(tabela_clientes, tabela_vendas, on='id_cliente', how='left')
tabela_primaria = pd.merge(tabela_primaria, tabela_produtos, on='id_produto', how='left')


# ==========================================================
# PARTE 5: SALVANDO OS RESULTADOS LIMPOS
# ==========================================================

tabela_clientes.to_csv("tbl_clientes_limpo.csv", index=False)
tabela_produtos.to_csv("tbl_produtos_limpo.csv", index=False)
tabela_vendas.to_csv("tbl_vendas_limpo.csv", index=False)
tabela_primaria.to_csv("tbl_primaria_limpa.csv", index=False)