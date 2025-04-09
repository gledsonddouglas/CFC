import streamlit as st
from xhtml2pdf import pisa
import os
import io
from datetime import datetime

# Configurações de login
USUARIOS = {
    "Tech360": "senha123",
    "Gledson": "1234"
}

def verificar_login(usuario, senha):
    return USUARIOS.get(usuario) == senha

def salvar_html_como_pdf(source_html):
    output = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(source_html), dest=output)
    if not pisa_status.err:
        return output.getvalue()
    return None

def calcular_custo(valor, quantidade_total, quantidade_usada):
    try:
        custo_unitario = valor / quantidade_total
        return custo_unitario * quantidade_usada
    except:
        return 0.0

def gerar_html_ficha(nome_produto, ingredientes, custo_total, rendimento, preco_unitario, modo_preparo):
    html = f"""
    <h1>Ficha Técnica: {nome_produto}</h1>
    <ul>
    """
    for ingr in ingredientes:
        html += f"<li>Ingrediente: {ingr['nome']} | Quantidade usada: {ingr['qtd_usada']} {ingr['unidade']} | Custo: R$ {ingr['custo']:.2f}</li>"
    html += f"""
    </ul>
    <p><strong>Custo total da receita:</strong> R$ {custo_total:.2f}</p>
    <p><strong>Rendimento:</strong> {rendimento}</p>
    <p><strong>Preço sugerido:</strong> R$ {preco_unitario:.2f}</p>
    <p><strong>Modo de Preparo:</strong><br>{modo_preparo}</p>
    """
    return html

def painel_usuario(usuario):
    st.title("Cadastrar Ficha Técnica")
    nome_produto = st.text_input("Nome do produto:")

    qtd_ingredientes = st.number_input("Quantos ingredientes deseja adicionar?", min_value=1, step=1)

    ingredientes = []
    custo_total = 0.0

    for i in range(int(qtd_ingredientes)):
        st.subheader(f"Ingrediente {i+1}")
        nome = st.text_input(f"Nome do ingrediente {i+1}:", key=f"nome_{i}")
        valor = st.number_input(f"Valor do ingrediente (R$):", min_value=0.0, key=f"valor_{i}")
        qtd_total = st.number_input(f"Quantidade total do ingrediente adquirido:", min_value=0.01, key=f"qtd_total_{i}")
        unidade = st.selectbox("Unidade de medida:", ["g", "kg", "ml", "l", "unidade"], key=f"unidade_{i}")
        qtd_usada = st.number_input(f"Quantidade usada na receita:", min_value=0.0, key=f"qtd_usada_{i}")

        custo = calcular_custo(valor, qtd_total, qtd_usada)
        custo_total += custo

        ingredientes.append({
            "nome": nome,
            "valor": valor,
            "qtd_total": qtd_total,
            "qtd_usada": qtd_usada,
            "unidade": unidade,
            "custo": custo
        })

    rendimento = st.number_input("Quantidade produzida com essa receita:", min_value=1.0)
    lucro = st.slider("Porcentagem de lucro desejado (%):", 0, 200, 0)

    custo_unitario = custo_total / rendimento
    preco_venda = custo_unitario + (custo_unitario * lucro / 100)

    st.markdown(f"**Custo total da receita:** R$ {custo_total:.2f}")
    st.markdown(f"**Preço de venda sugerido por unidade:** R$ {preco_venda:.2f}")

    modo_preparo = st.text_area("Modo de preparo")

    if st.button("Gerar Ficha Técnica em PDF"):
        html = gerar_html_ficha(nome_produto, ingredientes, custo_total, rendimento, preco_venda, modo_preparo)
        pdf_data = salvar_html_como_pdf(html)

        if pdf_data:
            st.success("PDF gerado com sucesso!")
            st.download_button(
                label="📥 Baixar Ficha Técnica em PDF",
                data=pdf_data,
                file_name=f"Ficha_Tecnica_{nome_produto}.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Erro ao gerar o PDF.")

def main():
    st.set_page_config(page_title="Sistema CFC", layout="centered")
    # fundo personalizado
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url('fundo.png');
            background-size: cover;
            background-position: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.title("Sistema CFC - Acesso Restrito")
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if verificar_login(usuario, senha):
                st.session_state.autenticado = True
                st.session_state.usuario = usuario
                st.success("Login realizado com sucesso!")
            else:
                st.error("Usuário ou senha inválidos!")
    else:
        st.image("logo.png", width=150)
        st.write(f"Bem-vindo, {st.session_state.usuario}!")
        painel_usuario(st.session_state.usuario)

if __name__ == "__main__":
    main()
