import streamlit as st
from openai import OpenAI
import os

# Chave da API da OpenAI

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="Chat com GPT-4o", layout="centered")
st.title("💬 Chat com GPT-4o")

# Inicializa estados
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversa_ativa" not in st.session_state:
    st.session_state.conversa_ativa = False
if "mostrar_mensagem_encerramento" not in st.session_state:
    st.session_state.mostrar_mensagem_encerramento = False

# Botões de controle da conversa
col1, col2 = st.columns(2)
with col1:
    if st.button("🟢 Iniciar conversa"):
        st.session_state.conversa_ativa = True
        st.session_state.mostrar_mensagem_encerramento = False
        st.session_state.messages = [
            {"role": "system", "content": "Você é um assistente útil."}
        ]

with col2:
    if st.button("🔴 Encerrar conversa"):
        st.session_state.conversa_ativa = False
        st.session_state.mostrar_mensagem_encerramento = True
        st.session_state.messages = []  # 🔥 limpa as mensagens exibidas

# Exibe mensagens anteriores (se houver)
if st.session_state.conversa_ativa:
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

# Campo de entrada de mensagem
if st.session_state.conversa_ativa:
    pergunta = st.chat_input("Digite sua pergunta...")
    if pergunta:
        with st.chat_message("user"):
            st.markdown(pergunta)
        st.session_state.messages.append({"role": "user", "content": pergunta})

        try:
            resposta = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages
            )
            conteudo_resposta = resposta.choices[0].message.content
            with st.chat_message("assistant"):
                st.markdown(conteudo_resposta)
            st.session_state.messages.append(
                {"role": "assistant", "content": conteudo_resposta}
            )

        except Exception as e:
            st.error(f"Erro ao consultar a API: {e}")

# Mensagem de encerramento
if st.session_state.mostrar_mensagem_encerramento:
    st.success("✅ Conversa encerrada. Obrigado por conversar conosco! Até a próxima.")
    st.session_state.mostrar_mensagem_encerramento = False  # Evita repetir
