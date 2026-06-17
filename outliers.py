import pandas as pd
import numpy as np

tabela = pd.read_csv("tbl_primaria_limpa.csv")

print(tabela)

# ==========================================================
# 1. TRATAMENTO DE OUTLIERS - QUANTIDADE (COM TRAVA MÍNIMA DE 8)
# ==========================================================
q1_q = tabela.groupby('nome_produto')['quantidade'].transform(lambda x: x.quantile(0.25))
q3_q = tabela.groupby('nome_produto')['quantidade'].transform(lambda x: x.quantile(0.75))
IQR_q = q3_q - q1_q
limite_normal_q = q3_q + (1.5 * IQR_q)

limite_alto_q = np.maximum(limite_normal_q, 8)
limite_baixo_q = q1_q - (1.5 * IQR_q)
mediana_q = tabela.groupby('nome_produto')['quantidade'].transform(lambda x: x.median())

# ==========================================================
# 2. TRATAMENTO DE OUTLIERS - PREÇO UNITÁRIO
# ==========================================================
q1_p = tabela.groupby('nome_produto')['preco_unitario'].transform(lambda x: x.quantile(0.25))
q3_p = tabela.groupby('nome_produto')['preco_unitario'].transform(lambda x: x.quantile(0.75))
IQR_p = q3_p - q1_p

limite_alto_p = q3_p + (1.5 * IQR_p)
limite_baixo_p = q1_p - (1.5 * IQR_p)
mediana_p = tabela.groupby('nome_produto')['preco_unitario'].transform(lambda x: x.median())

# --- PRINTS DIAGNÓSTICOS (Perfeitos) ---
print(f"Outliers de quantidade que serão tratados: \n{tabela[tabela['quantidade'] > limite_alto_q]}")
print(f"Outliers de preço Unitario que serão tratados: \n{tabela[tabela['preco_unitario'] > limite_alto_p]}")

# --- APLICAÇÃO DA LIMPEZA (Perfeita) ---
tabela['quantidade'] = np.where((tabela['quantidade'] > limite_alto_q) | (tabela['quantidade'] < limite_baixo_q), mediana_q, tabela['quantidade'])
tabela['preco_unitario'] = np.where((tabela['preco_unitario'] > limite_alto_p) | (tabela['preco_unitario'] < limite_baixo_p), mediana_p, tabela['preco_unitario'])

# --- SALVAMENTO PARA O DASHBOARD ---
tabela.to_csv("tabela_power_bi.csv", index=False)

print("\nBase de dados limpa e salva com sucesso para o Power BI!")