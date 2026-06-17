import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

tabela = pd.read_csv("tabela_power_bi.csv")

coluna = ['quantidade', 'preco_unitario']

corr_pearson = tabela[coluna].corr(method='pearson')
corr_spearman = tabela[coluna].corr(method='spearman')
valor_spearman = corr_spearman.loc['quantidade', 'preco_unitario']

print("\n--- MATRIZ DE CORRELAÇÃO (PEARSON) ---")
print(corr_pearson)
print("\n--- MATRIZ DE CORRELAÇÃO (SPEARMAN) ---")
print(corr_spearman)

plt.figure(figsize=(10, 6))

sns.set_theme(style='whitegrid')

sns.regplot(

    data=tabela,
    x='preco_unitario',
    y='quantidade',
    scatter_kws={'alpha':0.5, 'color': 'blue'},
    line_kws={'color': 'red', 'linewidth': 2},
    lowess=True

)

plt.title("Relação entre Preço Unitário e Quantidade Vendida (Pós-Limpeza)", fontsize=16, fontweight='bold', pad=15)
plt.xlabel("Preço Unitario R$", fontsize=12)
plt.ylabel("Quantidade Vendida (Unidades)", fontsize=12)

plt.text(x=tabela['preco_unitario'].min(), 
         y=tabela['quantidade'].max(), 
         s=f'Correlação de Spearman: {valor_spearman:.2f}', 
         fontsize=12, fontweight='bold', color='darkred',
         bbox=dict(facecolor='white', alpha=0.8))

plt.show()