import pandas as pd
import numpy as np

# --- CARREGAMENTO ---
tabela = pd.read_csv("tbl_primaria_limpa.csv")
print("Dados carregados com sucesso!")

# ==========================================================
# 1. CÁLCULO DE LIMITES (IQR POR PRODUTO)
# ==========================================================
# Quantidade
q1_q = tabela.groupby('nome_produto')['quantidade'].transform(lambda x: x.quantile(0.25))
q3_q = tabela.groupby('nome_produto')['quantidade'].transform(lambda x: x.quantile(0.75))
limite_alto_q = np.maximum(q3_q + (1.5 * (q3_q - q1_q)), 8)
limite_baixo_q = q1_q - (1.5 * (q3_q - q1_q))
mediana_q = tabela.groupby('nome_produto')['quantidade'].transform('median')

# Preço Unitário
q1_p = tabela.groupby('nome_produto')['preco_unitario'].transform(lambda x: x.quantile(0.25))
q3_p = tabela.groupby('nome_produto')['preco_unitario'].transform(lambda x: x.quantile(0.75))
limite_alto_p = q3_p + (1.5 * (q3_p - q1_p))
limite_baixo_p = q1_p - (1.5 * (q3_p - q1_p))
mediana_p = tabela.groupby('nome_produto')['preco_unitario'].transform('median')

# ==========================================================
# 2. IDENTIFICAÇÃO E REGISTRO DE OUTLIERS
# ==========================================================
mask_qtd = (tabela['quantidade'] > limite_alto_q) | (tabela['quantidade'] < limite_baixo_q)
mask_prc = (tabela['preco_unitario'] > limite_alto_p) | (tabela['preco_unitario'] < limite_baixo_p)

# Salvando os registros alterados para conferência futura
outliers = tabela[mask_qtd | mask_prc].copy()

# ==========================================================
# 3. APLICAÇÃO DA LIMPEZA (CIRURGIA NOS DADOS)
# ==========================================================
tabela['quantidade'] = np.where(mask_qtd, mediana_q, tabela['quantidade'])
tabela['preco_unitario'] = np.where(mask_prc, mediana_p, tabela['preco_unitario'])

# --- DIAGNÓSTICO FINAL ---
print(f"\nTotal de registros alterados: {len(outliers)}")

# ==========================================================
# 4. EXPORTAÇÃO DOS ARQUIVOS
# ==========================================================

tabela.to_csv("tabela_power_bi.csv", index=False)
outliers.to_csv("outliers.csv", index=False)