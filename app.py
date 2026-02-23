import streamlit as st
import anthropic

st.set_page_config(page_title="LUCIDBOT AI", page_icon="🚀")
st.title("🚀 LUCIDBOT — Asistente de Ventas")

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Pregúntame sobre tus ventas..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system="Eres el asistente de LUCIDBOT. Analiza ventas. Responde en español.",
            messages=st.session_state.messages
        ) as stream:
            for text in stream.text_stream:
                full_response += text
                placeholder.write(full_response + "▌")
        placeholder.write(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
