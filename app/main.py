import streamlit as st
from streamlit_chat import message
from utils import *
from langchain.chat_models import ChatVertexAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)

#Page Config
st.set_page_config(
     layout="wide",
     page_title="BBDW",
     #page_icon="https://api.dicebear.com/5.x/bottts-neutral/svg?seed=gptLAb"
)

#Sidebar
st.sidebar.header("About")
#st.sidebar.markdown(
#    "A place for me to experiment different LLM use cases, models, application frameworks and etc."
#)

#Main Page and Chatbot components
st.title("ChatBot usando VertexAI and TextEmbbedings")

if 'responses' not in st.session_state:
    st.session_state['responses'] = ["Como posso te ajudar?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

llm = ChatVertexAI(model_name="chat-bison")
if 'buffer_memory' not in st.session_state:
            st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)

system_msg_template = SystemMessagePromptTemplate.from_template(template="""Responda à pergunta da forma mais verdadeira possível usando o contexto fornecido,
e se a resposta não estiver contida no contexto, diga 'Desculpe! Não sei'""")
human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")
prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])
conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)

response_container = st.container()
textcontainer = st.container()

with textcontainer:
    query = st.text_input("Query: ", key="input")
    if query:
        with st.spinner("digitando..."):
            conversation_history = get_conversation_history()
            refined_query = query_refiner(conversation_history, query)
            st.subheader("Buca refinada:")
            st.write(refined_query)
            context = find_match(refined_query)
            response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")
        st.session_state.requests.append(query)
        st.session_state.responses.append(response) 

with response_container:
    if st.session_state['responses']:

        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i],key=str(i))
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')