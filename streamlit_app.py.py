import plotly.graph_objects as go
import streamlit as st

def calcular_custos(aluguel, salarios, outras_despesas, materia_prima, embalagens, comissoes, quantidade):
    # Custos Fixos
    cfc = aluguel + salarios + outras_despesas
    
    # Custos Variáveis Totais
    cvt = materia_prima + embalagens + comissoes
    
    # Custo Variável Médio por unidade
    cvm = cvt / quantidade if quantidade > 0 else 0
    
    # Custo Total do Produto
    ctp = cfc + cvt
    
    return cfc, cvm, ctp

# Interface com Streamlit
st.title("📊 Painel de Custos - MARMITA")

st.header("Custos Fixos")
aluguel = st.number_input("Aluguel (R$)", min_value=0.0, value=0.0, step=100.0)
salarios = st.number_input("Salários Fixos (R$)", min_value=0.0, value=0.0, step=100.0)
outras_despesas = st.number_input("Outras Despesas Fixas (R$)", min_value=0.0, value=0.0, step=100.0)

st.header("Custos Variáveis")
materia_prima = st.number_input("Matéria-prima (R$)", min_value=0.0, value=0.0, step=100.0)
embalagens = st.number_input("Embalagens (R$)", min_value=0.0, value=0.0, step=50.0)
comissoes = st.number_input("Comissões (R$)", min_value=0.0, value=0.0, step=50.0)
quantidade = st.number_input("Quantidade Produzida", min_value=1, value=1, step=1)

# Cálculo dos custos
cfc, cvm, ctp = calcular_custos(aluguel, salarios, outras_despesas, materia_prima, embalagens, comissoes, quantidade)

st.subheader("🔍 Resultados")
st.write(f"Custo Fixo Contábil (CFC): R$ {cfc:,.2f}")
st.write(f"Custo Variável Médio (CVM): R$ {cvm:,.2f} por unidade")
st.write(f"Custo Total do Produto (CTP): R$ {ctp:,.2f}")

# Gráfico de Pizza
labels = ['Custo Fixo Contábil', 'Custo Variável Total']
values = [cfc, materia_prima + embalagens + comissoes]
fig_pizza = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
fig_pizza.update_layout(title_text="Distribuição dos Custos")
st.plotly_chart(fig_pizza)

# Gráfico de Barras
labels_barras = ['Aluguel', 'Salários', 'Outras Despesas', 'Matéria-prima', 'Embalagens', 'Comissões']
values_barras = [aluguel, salarios, outras_despesas, materia_prima, embalagens, comissoes]
fig_barras = go.Figure([go.Bar(x=labels_barras, y=values_barras)])
fig_barras.update_layout(title_text="Detalhamento dos Custos", xaxis_title="Categorias", yaxis_title="Valor em R$")
st.plotly_chart(fig_barras)
