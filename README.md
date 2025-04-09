# 📊 Dashboard de Análise da Nota Fiscal Paulista

Este projeto é uma visualização interativa e moderna dos dados da Nota Fiscal Paulista. Desenvolvido com **Python**, **Streamlit** e **Plotly**, o painel permite ao usuário explorar dados relevantes sobre a emissão de notas e geração de créditos.

---

## 🗂️ 1. Coleta de Dados

Os dados utilizados foram previamente disponibilizados e carregados no formato `.csv`. A base foi estruturada com as seguintes colunas principais:

- **Data da Nota**
- **Valor da Nota**
- **Créditos Gerados**
- **Categoria do Estabelecimento**
- **Dia da Semana**
- **Flag de Crédito (0 ou 1)**

Os dados foram limpos e tratados para permitir visualizações precisas e categorização adequada dos registros.

---

## 🧩 2. Modelagem

Embora o foco principal do projeto tenha sido a **visualização de dados**, algumas etapas de modelagem de dados foram realizadas para facilitar a análise:

- **Criação de variáveis derivadas**:
  - Conversão da data da nota para o dia da semana (`Dia_Semana`)
  - Transformação de colunas categóricas
- **Filtragem de registros**:
  - Apenas notas com valor positivo e com crédito gerado foram usadas em certos gráficos

As ferramentas e bibliotecas utilizadas foram:

- `streamlit` para criação do dashboard interativo
- `pandas` e `numpy` para manipulação dos dados
- `plotly.express` para geração dos gráficos interativos
- `datetime` para tratamento de datas

---

## 📈 3. Visualizações

As principais visualizações implementadas no painel incluem:

- **Distribuição de Notas por Categoria**
- **Geração de Créditos ao Longo do Tempo**
- **Distribuição de Créditos por Dia da Semana**
- **Boxplot de Créditos por Categoria**
- **Correlação entre Valor da Nota e Créditos Gerados**

Todas as visualizações foram pensadas para facilitar insights visuais e possibilitar a exploração dinâmica por parte do usuário.

---

## ✅ 4. Conclusões

- A maior geração de créditos está concentrada em algumas categorias específicas.
- Os valores das notas e os créditos nem sempre têm uma relação direta, evidenciado pela dispersão nos gráficos.
- Dias úteis apresentam maior concentração de emissão de notas fiscais, principalmente durante a semana.

---

## 🚀 Deploy

O projeto foi publicado utilizando **Streamlit Cloud** e está disponível em:  
👉 [**Link para o App**](https://jowguhprojetosemantix.streamlit.app/)



## 💻 Requisitos

As bibliotecas necessárias para executar o projeto estão no arquivo `requirements.txt`:

