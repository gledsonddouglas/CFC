import streamlit as st
from xhtml2pdf import pisa
import io
import base64

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

def calcular_custo(valor_pago, qtd_usada):
    try:
        return valor_pago * qtd_usada
    except:
        return 0.0

def formatar_reais(valor):
    return f"R$ {valor:,.2f}".replace('.', ',')

def gerar_html_ficha(cliente, itens, custo_total, rendimento, preco_unitario, detalhes):
    html = f"""
    <h1>Ficha Técnica: {cliente}</h1>
    <ul>
    """
    for item in itens:
        html += f"<li>Item: {item['nome']} | Quantidade usada: {item['qtd_usada']} | Valor Pago: {formatar_reais(item['valor_pago'])} | Custo: {formatar_reais(item['custo'])}</li>"
    html += f"""
    </ul>
    <p><strong>Custo total do projeto:</strong> {formatar_reais(custo_total)}</p>
    <p><strong>Quantidade produzida:</strong> {rendimento}</p>
    <p><strong>Preço sugerido por unidade:</strong> {formatar_reais(preco_unitario)}</p>
    <p><strong>Detalhes do projeto:</strong><br>{detalhes}</p>
    """
    return html

def painel_usuario(usuario):
    st.title("Precificação de Projeto")
    st.image("logo.png", width=120)

    cliente_nome = st.text_input("Nome do cliente:")
    if "itens" not in st.session_state:
        st.session_state.itens = []

    with st.form("novo_item_form"):
        st.subheader("Adicionar novo item")
        nome_item = st.text_input("Item:")
        valor_pago = st.number_input("Valor pago (R$):", min_value=0.0, step=0.01, format="%.2f")
        qtd_usada = st.number_input("Quantidade usada:", min_value=0.0, step=0.01)
        adicionar = st.form_submit_button("Adicionar item")

        if adicionar:
            custo = calcular_custo(valor_pago, qtd_usada)
            st.session_state.itens.append({
                "nome": nome_item,
                "valor_pago": valor_pago,
                "qtd_usada": qtd_usada,
                "custo": custo
            })
            st.success(f"Item '{nome_item}' adicionado com sucesso!")

    st.subheader("Itens adicionados")
    custo_total = 0.0
    for idx, item in enumerate(st.session_state.itens):
        st.markdown(f"- **{item['nome']}** | Qtd usada: {item['qtd_usada']} | Valor pago: {formatar_reais(item['valor_pago'])} | Custo: {formatar_reais(item['custo'])}")
        if st.button(f"Excluir {item['nome']}", key=f"delete_{idx}"):
            del st.session_state.itens[idx]
            st.success(f"Item '{item['nome']}' excluído com sucesso!")
            break
        custo_total += item["custo"]

    rendimento = st.number_input("Quantidade produzida com esse projeto:", min_value=1.0, step=1.0)
    lucro = st.slider("Porcentagem de lucro desejado (%):", 0, 1000, 0)

    custo_unitario = custo_total / rendimento
    preco_venda = custo_unitario + (custo_unitario * lucro / 100)

    st.markdown(f"**Custo total do projeto:** {formatar_reais(custo_total)}")
    st.markdown(f"**Preço de venda sugerido por unidade:** {formatar_reais(preco_venda)}")

    detalhes = st.text_area("Detalhes do projeto")

    if st.button("Gerar Ficha Técnica em PDF"):
        html = gerar_html_ficha(cliente_nome, st.session_state.itens, custo_total, rendimento, preco_venda, detalhes)
        pdf_data = salvar_html_como_pdf(html)

        if pdf_data:
            st.success("PDF gerado com sucesso!")
            st.download_button(
                label="📥 Baixar Ficha Técnica em PDF",
                data=pdf_data,
                file_name=f"Ficha_Tecnica_{cliente_nome}.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Erro ao gerar o PDF.")

def carregar_imagem_base64(caminho_imagem):
    with open(caminho_imagem, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def background_carrossel():
    imagem_base64 = carregar_imagem_base64("static/foto3.jpeg")  # Usando foto3.jpeg como fundo
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{imagem_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            height: 100vh;
        }}
        .logo-wrapper {{
            z-index: 1;
            position: absolute;
            top: 20px;
            left: 20px;
        }}
        .login-box {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 2rem;
            border-radius: 10px;
            max-width: 400px;
            margin: auto;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    st.set_page_config(page_title="Sistema de Precificação", layout="centered")

    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        background_carrossel()
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.title("Douglas Luciano - Precificação 7.0")
        st.subheader("Acesso Restrito")
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if verificar_login(usuario, senha):
                st.session_state.autenticado = True
                st.session_state.usuario = usuario
                st.success("Login realizado com sucesso!")
            else:
                st.error("Usuário ou senha inválidos!")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Após o login, mantém o fundo e exibe o conteúdo
        background_carrossel()
        painel_usuario(st.session_state.usuario)

if __name__ == "__main__":
    main()
