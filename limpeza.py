import pandas as pd
import numpy as np

# Carregamento dos dados brutos
tabela_clientes = pd.read_csv("tbl_clientes_sujo.csv")
tabela_produtos = pd.read_csv("tbl_produtos_sujo.csv")
tabela_vendas = pd.read_csv("tbl_vendas_sujo.csv")

# ==========================================================
# PARTE 1: LIMPEZA DOS CLIENTES (NOME, ESTADO E E-MAILS)
# ==========================================================

# Visualização inicial e diagnóstico da tabela de clientes
print(tabela_clientes)
print(tabela_clientes.shape)
tabela_clientes.info()
print(tabela_clientes.isnull().sum())

# --- TRATAMENTO DOS NOMES DOS CLIENTES ---
# Remove espaços extras nas pontas e padroniza para formato de título (Primeira Letra Maiúscula)
print(tabela_clientes['nome_cliente'])
tabela_clientes['nome_cliente'] = tabela_clientes['nome_cliente'].str.strip().str.title()
print(tabela_clientes['nome_cliente'])
print(tabela_clientes['nome_cliente'].unique())

# --- TRATAMENTO DOS ESTADOS E SIGLAS ---
# 1. Remove espaços em branco antes de validar as siglas
print(tabela_clientes['estado'])
tabela_clientes['estado'] = tabela_clientes['estado'].str.strip()
print(tabela_clientes['estado'])
print(tabela_clientes['estado'].unique())

# Dicionário de tradução para tratar estados por extenso ou abreviações fora do padrão
estado_sigla = {
    'Rio de Janeiro': 'RJ',
    'S.Paulo': 'SP',
    'São Paulo': 'SP',
    'Minas Gerais': 'MG'
}

# 2. Identifica registros inválidos (que NÃO possuem o formato de sigla com exatamente 2 letras)
estado_errado = ~tabela_clientes['estado'].str.contains(r'^[a-zA-Z]{2}$', regex=True, na=False)

# 3. Mapeia e corrige apenas os estados fora do padrão usando o dicionário
tabela_clientes.loc[estado_errado, 'estado'] = tabela_clientes.loc[estado_errado, 'estado'].map(estado_sigla)

# 4. Força todas as siglas para letras maiúsculas
tabela_clientes['estado'] = tabela_clientes['estado'].str.upper()

print(tabela_clientes[tabela_clientes['estado'].isna()])
print(tabela_clientes['estado'].unique())
print(tabela_clientes['estado'])

# --- VALIDAÇÃO E LIMPEZA DE E-MAILS (CONTAINS + DROP DUPLICATES) ---
# 1. Primeiro identificamos e invalidamos e-mails sem o caractere '@'
tabela_clientes['email'] = np.where(~tabela_clientes['email'].str.contains("@", na=False), pd.NA, tabela_clientes['email'])

# 2. Depois removemos as linhas duplicadas (mantendo apenas o primeiro registro válido)
com_email = tabela_clientes[tabela_clientes['email'].notna()]
sem_email = tabela_clientes[tabela_clientes['email'].isna()]
print(f"Duplicados antes: {com_email.duplicated().sum()}")
com_email = com_email.drop_duplicates(subset='email', keep='first')
print(f"Duplicados depois: {com_email.duplicated().sum()}")

# Unifica a base de clientes novamente juntando registros válidos e nulos
tabela_clientes = pd.concat([com_email, sem_email], ignore_index=True)

# --- VALIDAÇÃO FINAL DA TABELA DE CLIENTES ---
print(tabela_clientes)
print(tabela_clientes.shape)
tabela_clientes.info()
print(tabela_clientes.isnull().sum())


# ==========================================================
# PARTE 2: LIMPEZA DOS PRODUTOS (CATEGORIAS E PREÇOS)
# ==========================================================

# Visualização inicial e diagnóstico da tabela de produtos
print(tabela_produtos)
print(tabela_produtos.shape)
tabela_produtos.info()
print(tabela_produtos.isnull().sum())

# Padroniza textos de nomes e categorias removendo espaços e aplicando formato Title
tabela_produtos['nome_produto'] = tabela_produtos['nome_produto'].str.strip().str.title()
tabela_produtos['categoria'] = tabela_produtos['categoria'].str.strip().str.title()

# Transforma a marcação de erro '???' em um nulo real (NaN) temporário
tabela_produtos['categoria'] = tabela_produtos['categoria'].replace('???', np.nan)

print(tabela_produtos['nome_produto'].unique())
print(tabela_produtos['categoria'].unique())

# --- TRATAMENTO AUTOMATIZADO DE CATEGORIAS (LOGICA DA MODA ESTATÍSTICA) ---
# 1. Filtra apenas registros que possuem categorias preenchidas corretamente
produtos_validos = tabela_produtos.dropna(subset=['categoria'])

# 2. Agrupa por nome do produto e mapeia a categoria que mais se repete (Moda), evitando falhas manuais de preenchimento
mapeamento = produtos_validos.groupby('nome_produto')['categoria'].agg(lambda x: x.mode()[0])

# 3. Cria a série de socorro e aplica o fillna para consertar os antigos '???'
mapeamento_socorro = tabela_produtos['nome_produto'].map(mapeamento)
tabela_produtos['categoria'] = tabela_produtos['categoria'].fillna(mapeamento_socorro)

print(tabela_produtos)
print(tabela_produtos['categoria'].isnull().sum())

# --- TRATAMENTO DOS PREÇOS DE CUSTO ---
# Limpa strings de moeda (R$), altera o separador decimal para ponto e converte para float
tabela_produtos['preco_custo'] = tabela_produtos['preco_custo'].str.replace('R$', '', regex=False)
tabela_produtos['preco_custo'] = tabela_produtos['preco_custo'].str.replace(',', '.', regex=False)
tabela_produtos['preco_custo'] = tabela_produtos['preco_custo'].astype(float)

print(tabela_produtos['preco_custo'])
print(tabela_produtos[tabela_produtos['preco_custo'] < 0])

# --- VALIDAÇÃO FINAL DA TABELA DE PRODUTOS ---
print(tabela_produtos)
print(tabela_produtos.shape)
tabela_produtos.info()
print(tabela_produtos.isnull().sum())
print(tabela_produtos.describe())


# ==========================================================
# PARTE 3: LIMPEZA DAS VENDAS (DATAS, QUANTIDADES E DESCONTOS)
# ==========================================================

# Visualização inicial e diagnóstico da tabela de vendas
print(tabela_vendas)
print(tabela_vendas.shape)
tabela_vendas.info()
print(tabela_vendas.isnull().sum())

print(tabela_vendas['data_venda'])

# --- TRATAMENTO E VALIDAÇÃO DE DATAS ---
# Cria coluna auxiliar formatada e converte a original para o tipo datetime (forçando erros bizarros a virarem NaT)
tabela_vendas['data_venda_formatada'] = tabela_vendas['data_venda'].replace(r'(\d{4})-(\d{2})-(\d{2})', r'\3/\2/\1', regex=True)
tabela_vendas['data_venda'] = pd.to_datetime(tabela_vendas['data_venda'], errors='coerce')

print(tabela_vendas['data_venda_formatada'])

# Filtra o DataFrame para remover vendas futuras absurdas acima do ano atual
tabela_vendas = tabela_vendas[tabela_vendas['data_venda'].dt.year <= 2026]

# --- TRATAMENTO DE QUANTIDADES ---
print(tabela_vendas['quantidade'])
print(tabela_vendas[tabela_vendas['quantidade'] < 0])

# Calcula a mediana apenas de quantidades válidas (maiores ou iguais a zero)
mediana = tabela_vendas.loc[tabela_vendas['quantidade'] >= 0, 'quantidade'].median()

# Substitui quantidades negativas pela mediana geral calculada
tabela_vendas['quantidade'] = np.where(tabela_vendas['quantidade'] < 0, mediana, tabela_vendas['quantidade'])

print(tabela_vendas[tabela_vendas['quantidade'] < 0])

# --- VALIDAÇÃO DE PREÇOS E DESCONTOS ---
print(tabela_vendas['preco_unitario'])
print(f"Preço negativo: \n{tabela_vendas[tabela_vendas['preco_unitario'] < 0]}")

print(tabela_vendas['desconto_percent'])
print(tabela_vendas[tabela_vendas['desconto_percent'].isna()])

# Preenche descontos ausentes (NaN) com o valor padrão de 0%
tabela_vendas['desconto_percent'] = tabela_vendas['desconto_percent'].fillna(0)

print(tabela_vendas['desconto_percent'])
print(tabela_vendas[tabela_vendas['desconto_percent'].isna()])

# Verificação de inconsistências no valor de frete
print(tabela_vendas['frete'])
print(tabela_vendas[tabela_vendas['frete'].isna()])
print(tabela_vendas[tabela_vendas['frete'] < 0])


# ==========================================================
# PARTE 4: CONSOLIDANDO AS BASES (O MERGE DO CHEFE)
# ==========================================================

print(f"Tabela clientes: \n{tabela_clientes}")
print(f"Tabela vendas: \n{tabela_vendas}")
print(f"Tabela produtos: \n{tabela_produtos}")

# Unifica as bases de dados usando a tabela de vendas como a principal (Fato)
tabela_primaria = pd.merge(tabela_vendas, tabela_produtos, on='id_produto', how='left')
tabela_primaria = pd.merge(tabela_primaria, tabela_clientes, on='id_cliente', how='left')

# Elimina registros correspondentes a produtos fantasmas que não constavam no cadastro
tabela_primaria = tabela_primaria.dropna(subset=['nome_produto'])


# ==========================================================
# PARTE 5: SALVANDO OS RESULTADOS LIMPOS
# ==========================================================

tabela_clientes.to_csv("tbl_clientes_limpo.csv", index=False)
tabela_produtos.to_csv("tbl_produtos_limpo.csv", index=False)
tabela_vendas.to_csv("tbl_vendas_limpo.csv", index=False)
tabela_primaria.to_csv("tbl_primaria_limpa.csv", index=False)