import streamlit as st
from groq import Groq

# ================================
# 1) Configuración inicial
# ================================
st.set_page_config(page_title="Chat con Memoria", page_icon="🤖")

# Cliente Groq usando clave de secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ================================
# 2) Manejo de estado (historial)
# ================================
if "messages" not in st.session_state:
    st.session_state.messages = []  # Lista de turnos de conversación

# ================================
# 3) Mostrar historial
# ================================
st.title("🤖 Chatbot con Memoria (Stateful)")
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================================
# 4) Entrada del usuario
# ================================
if prompt := st.chat_input("Escribe tu mensaje..."):
    # Añadir mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ================================
    # 5) Enviar historial al modelo Groq
    # ================================
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=st.session_state.messages
    )

    # Obtener respuesta
    reply = response.choices[0].message.content

    # Añadir respuesta al historial
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # Mostrar respuesta
    with st.chat_message("assistant"):
        st.markdown(reply)
