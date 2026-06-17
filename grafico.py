import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- CARREGAMENTO ---
tabela = pd.read_csv("tabela_power_bi.csv")
print("Dados carregados para análise de correlação!")

# ==========================================================
# 1. CÁLCULO DA CORRELAÇÃO (SPEARMAN)
# ==========================================================
# Agrupamos por produto e calculamos a correlação entre as duas colunas
matriz_corr = tabela.groupby('nome_produto')[['preco_unitario', 'quantidade']].corr(method='spearman')

# "Desembrulhamos" a matriz para um formato de tabela plana (DataFrame comum)
matriz_limpa = matriz_corr.unstack()

# Selecionamos especificamente a correlação de interesse
correlacoes_finais = matriz_limpa.loc[:, ('quantidade', 'preco_unitario')]

# Exibição no console
print("\n--- Matriz de Correlação (Spearman) ---")
print(matriz_corr)

# ==========================================================
# 2. VISUALIZAÇÃO GRÁFICA
# ==========================================================
plt.figure(figsize=(10, 6))
sns.set_theme(style='whitegrid')

# Regplot com suavização (LOWESS) para capturar tendências não lineares
sns.regplot(
    data=tabela,
    x='preco_unitario',
    y='quantidade',
    scatter_kws={'alpha': 0.5, 'color': 'blue'},
    line_kws={'color': 'red', 'linewidth': 2},
    lowess=True
)

plt.title("Relação entre Preço Unitário e Quantidade Vendida", fontsize=16, fontweight='bold', pad=15)
plt.xlabel("Preço Unitário (R$)", fontsize=12)
plt.ylabel("Quantidade Vendida (Unidades)", fontsize=12)

plt.show()

# ==========================================================
# 3. EXPORTAÇÃO DO RESULTADO
# ==========================================================
matriz_limpa.to_csv("correlacoes.csv", index=True)

print("\nAnálise concluída: arquivo 'correlacoes.csv' gerado com sucesso!")