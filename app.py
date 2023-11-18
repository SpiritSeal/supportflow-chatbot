import streamlit as st
import os
from openai import AzureOpenAI

from functions import call_function

st.title("Support Chat UI")
# when will my order be delivered?, colin.flueck@gmail.com W123123

functions = [
    {
        "name": "order_tracking_status",
        "description": "Retrieves the status of an order based on **both** the email address and order number.",
        "parameters": {
            "type": "object",
            "properties": {
                "email_address": {
                    "type": "string",
                    "description": "The email address associated with the order"
                },
                "order_number": {
                    "type": "string",
                    "description": "The order number. For online orders, this starts with either the letter W or C. "
                                   "For in-store orders, this starts with the letter H. You can find your order "
                                   "number in your confirmation email or your receipt."
                },
            },
            "required": ["email_address, order_number"]
        }
    }
]

client = AzureOpenAI(
    api_key=os.environ['OPENAI_API_KEY'],
    api_version="2023-07-01-preview",
    azure_endpoint=os.environ['AZURE_ENDPOINT'],
)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-35-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful customer support agent for "
                                                               "The Home Depot. Be as helpful as possible and call "
                                                               "functions when necessary."},]

for message in st.session_state.messages:
    if message["role"] == "assistant" or message["role"] == "user":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("How can we help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🏠"):  # avatar=st.image('Home-Depot-Logo.png', width=50)):
        message_placeholder = st.empty()
        full_message = ""
        func_call = {
            "name": None,
            "arguments": "",
        }

        called_function = True
        while called_function:
            called_function = False
            for response in client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=[
                {"role": m["role"], "content": m["content"], "name": m["name"]} if "name" in m else
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
                    functions=functions,
                    function_call="auto",
                    stream=True,
            ):
                if len(response.choices) > 0:
                    delta = response.choices[0].delta

                    full_message += (delta.content or "")
                    if delta.function_call is not None:
                        if delta.function_call.name is not None:
                            func_call["name"] = delta.function_call.name
                        if delta.function_call.arguments is not None:
                            func_call["arguments"] += delta.function_call.arguments
                    if response.choices[0].finish_reason == "function_call" and func_call["name"] is not None:
                        print(f"Function generation requested, calling function")
                        function_response = call_function(st.session_state.messages, func_call)
                        print("function response")
                        print(function_response)
                        st.session_state.messages.append(function_response)
                        called_function = True

                    message_placeholder.markdown(full_message + "▌")

        message_placeholder.markdown(full_message)

        st.session_state.messages.append({"role": "assistant", "content": full_message})
