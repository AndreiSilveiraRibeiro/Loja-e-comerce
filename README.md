# Loja e-comerce

Este projeto compreende o desenvolvimento de um **pipeline de dados (ETL)** e **análise estatística** avançada para um **e-commerce**, com o objetivo de **higienizar bases** de dados de vendas, identificar anomalias e extrair inteligência sobre a relação entre preço e volume de vendas.

![Dashboard de E-comerce](dashboard.png)

# 🛠 Tecnologias Utilizadas

- **Linguagem:** Python

- **Bibliotecas:** Pandas, NumPy, Seaborn, Matplotlib

- **Ferramenta de BI:** Power BI

- **Técnicas:** ETL, IQR (Intervalo Interquartil), Correlação de Spearman, Visualização de Tendências

# ⚙️ Processo de Pipeline (ETL)

O fluxo de dados foi desenhado para garantir a qualidade analítica em um ambiente de e-commerce:

- **Higienização de Dados:** Tratamento de clientes, produtos e vendas, incluindo padronização de nomes (formato título), limpeza de strings e conversão de tipos de dados para assegurar consistência nas métricas.

- **Modelagem Relacional:** União das tabelas de Vendas, Clientes e Produtos (Left Join) para criação de uma base centralizada, eliminando registros órfãos que comprometiam a integridade do modelo.

- **Tratamento de Exceções:** Implementação de regras para lidar com valores nulos e inconsistências nos valores de frete e descontos, garantindo a fidelidade dos indicadores financeiros.

# 📊 Análise Estatística e Auditoria

A análise de dados focou em identificar o comportamento real do mercado através de técnicas robustas:

- **Detecção de Anomalias (IQR):** Aplicação do Intervalo Interquartil agrupado por produto para identificar variações atípicas em quantidade e preco_unitario. Valores fora dos limites estatísticos foram tratados para evitar distorções nas médias globais.

- **Correlação de Spearman:** Investigação da relação entre o preço unitário e o volume vendido. Esta técnica não paramétrica permitiu capturar tendências não lineares, essenciais para entender a sensibilidade do consumidor frente a variações de preço por categoria.

- **Visualização de Tendências:** Utilização de regplot com suavização (LOWESS) para identificar padrões de comportamento de compra que não seriam visíveis apenas com análises lineares.

# 📈 Insights do Dashboard

O dashboard no Power BI foi projetado para apoiar a estratégia comercial:

- **Métricas de Vendas:** Visão consolidada de descontos, fretes e margens.

- **Análise de Categoria:** Identificação dos produtos com melhor performance de saída e sua relação com a política de preços.

- **Auditoria de Outliers:** Identificação dos registros que sofreram intervenção estatística, permitindo ao time de vendas rastrear compras atípicas.

# 💡 Propostas de Melhoria para a Empresa

Com base nos padrões identificados, seguem as recomendações estratégicas:

- **Gestão Inteligente de Preços:** Utilizar a correlação entre preço e quantidade para realizar testes de elasticidade de demanda, otimizando a precificação por categoria.

- **Monitoramento Ativo:** Implementar o script de detecção de outliers como um alerta diário para evitar erros de cadastro de produtos ou falhas de processamento no sistema de vendas.

- **Refinamento de Logística:** Avaliar os registros tratados no frete para identificar possíveis falhas no cálculo de custo logístico ou taxas de envio excessivas.

### 📝 Autor

**Andrei - Analista de Dados / Desenvolvedor**