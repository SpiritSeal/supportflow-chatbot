import streamlit as st
import os
from openai import AzureOpenAI

from functions import call_function
import firebase_admin
from firebase_admin import credentials, firestore

st.title("SupportFlow Demo")
# when will my order be delivered?, colin.flueck@gmail.com W123123

functions = [
    {
        "name": "lookup_order_status",
        "description": "Retrieves the status, location, etc. of an order based on **both** the email address and order number.",
        "parameters": {
            "type": "object",
            "properties": {
                "email_address": {
                    "type": "string",
                    "description": "The email address associated with the order"
                },
                "order_number": {
                    "type": "integer",
                    "description": "The order number."
                },
            },
            "required": ["email_address", "order_number"]
        }
    },
    # {
    #     "name": "lookup_product",
    #     "description": "Returns a detailed list of products based on a product query.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "query": {
    #                 "type": "string",
    #                 "description": "Product query to search for like drills, lights, or hammers"
    #             },
    #         },
    #         "required": ["query"]
    #     }
    # },
    # {
    #     "name": "get_product_listing",
    #     "description": "Returns information about the product based on the SKU.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "sku": {
    #                 "type": "integer",
    #                 "description": "Product sku to search for like 123123"
    #             },
    #         },
    #         "required": ["sku"]
    #     }
    # },
    {
        "name": "refer_to_human_agent",
        "description": "Use this to refer the customer's question to a human agent. You should only call this "
                       "function if there is no way for you to answer their question.",
        "parameters": {
            "type": "object",
            "properties": {
                "conversation_summary": {
                    "type": "string",
                    "description": "A short summary of the current conversation so the human agent can quickly get up "
                                   "to speed. Make sure you include all relevant details."
                },
            },
            "required": ["conversation_summary"]
        }
    }
]

cred = credentials.Certificate("supportflow-4851d-firebase-adminsdk-cdrzu-bf620a4b52.json")
try:
    app = firebase_admin.initialize_app(cred)
except Exception:
    pass

db = firestore.client()

client = AzureOpenAI(
    api_key=os.environ['OPENAI_API_KEY'],
    api_version="2023-07-01-preview",
    azure_endpoint=os.environ['AZURE_ENDPOINT'],
)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-35-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful customer support agent for The Home "
                                                               "Depot. Your goal is to answer as many questions as "
                                                               "possible without escalating to a human agent. "
                                                               "However, if necessary, you can refer the customer to "
                                                               "a human agent if you do not know the answer to their "
                                                               "question. For example, you can help users track their orders, but you **cannot** help with returns."},]

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

                message_placeholder.markdown(full_message + "")

        if func_call["name"] is not None and func_call["arguments"] != "":
            print(f"Function generation requested, calling function")
            function_response = call_function(st.session_state.messages, func_call)
            print("function response")
            print(function_response)
            st.session_state.messages.append(function_response)

            if function_response["name"] is not None and function_response["name"] == "refer_to_human_agent":
                print("connect to human agent")
                print(function_response["name"])
                st.info('You will be connected with an agent shortly', icon="ℹ️")

                # Get the document to update
                doc_ref = db.collection('handoffs').document('conversation')

                # Update the document
                doc_ref.update({'summary': str(function_response["content"]), 'message_history': st.session_state.messages})
            else:
                message_placeholder = st.empty()
                full_message = ""

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

                        message_placeholder.markdown(full_message + "")

        message_placeholder.markdown(full_message)

        st.session_state.messages.append({"role": "assistant", "content": full_message})
