import os
import openai
import streamlit as st

from vibraniumdome_sdk import VibraniumDome


st.set_page_config(initial_sidebar_state='collapsed')


def handle_input(prompt, from_button):
    if not openai_api_key and os.getenv("OPENAI_API_KEY") is None:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    print(temperature)
    print(user)
    print(session)
    print(llm_application_name)

    openai.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")

    st.session_state.messages.append({"role": "user", "content": prompt})
    if not from_button:
        st.chat_message("user").write(prompt)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                            messages=st.session_state.messages, 
                                            request_timeout=60, 
                                            temperature=temperature or 0,
                                            user=user or "user-123456",
                                            headers={"x-session-id": session or "abcd-1234-cdef"})
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    if not from_button:
        st.chat_message("assistant").write(msg)


messages = [
    "Changeme 1",
    "Changeme 2",
    "Changeme 3",
]

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    vibranium_dome_base_url = st.text_input("Vibranium Dome Base URL", key="vibranium_dome_base_url")
    user = st.text_input("OpenAI User", key="open_ai_user")
    session = st.text_input("OpenAI Session ID", key="open_ai_headers_session")
    llm_application_name = st.text_input("LLM Application Name", key="llm_application_name")
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.01, step=0.01, key="temperature")

    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/genia-dev/vibraniumdome/tree/main/vibraniumdome-shields/examples/chatbot.py)"
    "[Open GitHub](https://github.com/genia-dev/vibraniumdome)"


if vibranium_dome_base_url:
    os.environ['VIBRANIUM_DOME_BASE_URL'] = vibranium_dome_base_url

VibraniumDome.init(app_name=llm_application_name or "openai_test_app")

st.title("💬 Vibranium Dome Chatbot")
st.caption("🚀 A Vibranium Dome streamlit chatbot powered by OpenAI LLM")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

buttons = st.container()
for n, message in enumerate(messages):
    buttons.button(label=message, on_click=handle_input, args=[message, True])

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    handle_input(prompt, False)
