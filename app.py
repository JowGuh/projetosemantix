import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime


st.set_page_config(
    page_title="Dashboard NFP - Visualização Moderna",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("semantix.png", width=850)  


@st.cache_data
def load_and_clean_data():
    
    df = pd.read_pickle('base_nfp.pkl')
    
    
    date_cols = ['Data Emissão', 'Data Registro']
    for col in date_cols:
        if not pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    
    df['Mês'] = df['Data Emissão'].dt.month
    df['Dia_Semana'] = df['Data Emissão'].dt.day_name()
    df['Mês_Ano'] = df['Data Emissão'].dt.to_period('M').astype(str)
    df['Dias_Registro'] = (df['Data Registro'] - df['Data Emissão']).dt.days
    
    
    num_cols = ['Valor NF', 'Créditos', 'Retorno', 'Dias_Registro']
    for col in num_cols:
        
        df[col] = df[col].replace([np.inf, -np.inf], np.nan)
        
        df[col] = df[col].fillna(df[col].median())
        
        if col in ['Valor NF', 'Créditos']:
            df[col] = df[col].clip(lower=0)
    
    
    df['categoria'] = df['categoria'].fillna('Outros')
    
    return df

df = load_and_clean_data()

paleta_roxo_azul = ['#7b68ee', '#6a5acd', '#483d8b', '#4169e1', '#4682b4',
                    '#5f9ea0', '#6495ed', '#87cefa', '#9370db', '#8a2be2']


st.title("Dashboard de Análise NFP")
st.markdown("""
Visualização interativa e moderna dos dados da Nota Fiscal Paulista.
""")
st.markdown("---")


st.header("Visão Geral dos Dados")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de Notas", f"{len(df):,}")
with col2:
    st.metric("Valor Total", f"R$ {df['Valor NF'].sum():,.2f}")
with col3:
    st.metric("Créditos Gerados", f"R$ {df['Créditos'].sum():,.2f}")


st.header("Análise Temporal")

tab1, tab2 = st.tabs(["Evolução Mensal", "Distribuição por Dia"])

with tab1:
    
    monthly_data = df.groupby('Mês_Ano').agg({
        'No.': 'count',
        'Valor NF': 'sum',
        'Créditos': 'sum'
    }).reset_index()
    
    fig = px.line(monthly_data, x='Mês_Ano', y='Valor NF',
                 title='Valor Total das Notas por Mês',
                 labels={'Valor NF': 'Valor Total (R$)', 'Mês_Ano': 'Mês/Ano'})
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    
    dias_traducao = {
        'Monday': 'Segunda',
        'Tuesday': 'Terça',
        'Wednesday': 'Quarta',
        'Thursday': 'Quinta',
        'Friday': 'Sexta',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }

    df['Dia_Semana_PT'] = df['Dia_Semana'].replace(dias_traducao)

    fig = px.histogram(
        df, 
        x='Dia_Semana_PT', 
        category_orders={'Dia_Semana_PT': 
                         ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']},
        title='Distribuição de Notas por Dia da Semana',
        color='Dia_Semana_PT',
        color_discrete_sequence=paleta_roxo_azul,
        labels={'Dia_Semana_PT': 'Dia da Semana'}
    )
    st.plotly_chart(fig, use_container_width=True)


st.header("Análise por Categoria")

col1, col2 = st.columns(2)




with col1:
    
    cat_value = df.groupby('categoria')['Valor NF'].sum().nlargest(10).reset_index()
    fig = px.bar(cat_value, x='Valor NF', y='categoria', orientation='h',
                title='Top 10 Categorias por Valor Total',
                labels={'Valor NF': 'Valor Total (R$)', 'categoria': 'Categoria'},
                color='categoria',
                color_discrete_sequence=paleta_roxo_azul)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    
    cat_credit = df.groupby('categoria')['Créditos'].mean().nlargest(10).reset_index()
    fig = px.bar(cat_credit, x='Créditos', y='categoria', orientation='h',
                title='Top 10 Categorias por Média de Créditos',
                labels={'Créditos': 'Média de Créditos (R$)', 'categoria': 'Categoria'},
                color='categoria',
                color_discrete_sequence=paleta_roxo_azul)
    st.plotly_chart(fig, use_container_width=True)


st.header("Média de Créditos por Categoria")


credit_df = df[df['flag_credito'] == 1].copy()


credit_df['Créditos'] = pd.to_numeric(credit_df['Créditos'], errors='coerce')

media_credito = credit_df.groupby("categoria")["Créditos"].mean().reset_index()

fig = px.bar(media_credito, x="categoria", y="Créditos",
             title="Média de Créditos por Categoria",
             labels={"Créditos": "Créditos Médios (R$)", "categoria": "Categoria"},
             color="Créditos", color_continuous_scale="Viridis")

st.plotly_chart(fig, use_container_width=True)

    

st.header("Correlações entre Variáveis")


num_df = df[['Valor NF', 'Créditos', 'Retorno', 'Dias_Registro']].corr()


fig = go.Figure(data=go.Heatmap(
    z=num_df.values,
    x=num_df.columns,
    y=num_df.columns,
    colorscale='Blues',
    hoverongaps=False
))


for i in range(len(num_df)):
    for j in range(len(num_df.columns)):
        fig.add_annotation(dict(
            x=num_df.columns[j],
            y=num_df.columns[i],
            text=str(round(num_df.values[i][j], 2)),
            showarrow=False,
            font=dict(color='black')
        ))

fig.update_layout(title='Mapa de Calor de Correlação')
st.plotly_chart(fig, use_container_width=True)






st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <p>© 2025 Dashboard NFP - Visualização Moderna</p>
    <p>Desenvolvido com Streamlit e Plotly</p>
    <p>PROJETO SEMANTIX</p>
    <p>by Jonathan Gustavo</p>
</div>
""", unsafe_allow_html=True)
