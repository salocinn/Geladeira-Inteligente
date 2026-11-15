import streamlit as st
from PIL import Image
from google import genai
import os

# Configuração da página do painel no navegador
st.set_page_title_config = st.set_page_config(page_title="Smart Fridge - UFPR", layout="centered")

st.title("🧊 Smart Fridge - Painel de Controle")
st.markdown("Projeto de Engenharia Elétrica / Sistemas Embarcados")

# Dica: Você pode definir a variável de ambiente GEMINI_API_KEY no seu sistema 
# ou colar sua chave diretamente aqui para testes rápidos.
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6JUjeIn8ZnWCOkw0dHEYzL01eX4PHUd82zEgOdVm9r0Kw"))

# --- SEÇÃO 1: TELEMETRIA (Simulada até o ESP32 chegar) ---
st.header("📊 Telemetria em Tempo Real")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="🌡️ Temperatura Interna", value="4.2 °C", delta="-0.5 °C (Ideal)")

with col2:
    st.metric(label="🚪 Estado da Porta", value="FECHADA", delta="Estável")

st.divider()

# --- SEÇÃO 2: RECONHECIMENTO DE ALIMENTOS POR FOTO (IA) ---
st.header("📸 Adicionar Alimentos por Foto (Visão Computacional)")
st.write("Tire uma foto do interior da geladeira ou das compras para a IA identificar os itens e estimar a validade.")

uploaded_file = st.file_uploader("Escolha uma foto...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Foto enviada da geladeira", use_column_width=True)
    
    if st.button("Analisar Alimentos com IA"):
        with st.spinner("A Inteligência Artificial está analisando os itens..."):
            try:
                # Chamada para o modelo Gemini analisar a imagem
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[
                        image,
                        "Analise esta foto do interior de uma geladeira. Liste todos os alimentos visíveis, "
                        "estime o tempo de validade aproximado de cada um a partir de agora, "
                        "e retorne o resultado em formato de lista clara."
                    ]
                )
                st.success("Análise concluída!")
                st.subheader("📦 Itens Identificados e Validade Estimada:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Erro ao conectar com a API: {e}")
                st.info("Certifique-se de configurar sua chave da API do Gemini corretamente no código.")

st.divider()

# --- SEÇÃO 3: SUGESTÃO DE RECEITAS ---
st.header("🍳 Sugestão de Receitas Inteligentes")
st.write("Com base no que você tem guardado, a IA sugere o que preparar.")

if st.button("Gerar Sugestão de Prato"):
    with st.spinner("Buscando receitas..."):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents="Sugira uma receita simples e prática que possa ser feita com ingredientes comuns de geladeira (ex: ovos, tomate, queijo, leite)."
            )
            st.info(response.text)
        except Exception as e:
            st.error("Configure sua chave da API para gerar as receitas.")