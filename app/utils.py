import os

import pinecone
import vertexai
import streamlit as st
from vertexai.language_models import TextGenerationModel
from vertexai.language_models import TextEmbeddingModel

model= TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"], environment=os.environ["PINECONE_ENV"]
)
index = pinecone.Index('bbdw')

def text_embedding(input) -> list:
    embeddings = model.get_embeddings([input])
    for embedding in embeddings:
        vector = embedding.values
        print(f"Length of Embedding Vector: {len(vector)}")
    return vector

def find_match(input):
    input_em = text_embedding(input)
    result = index.query(input_em, top_k=2, includeMetadata=True)
    return result['matches'][0]['metadata']['text']+"\n"+result['matches'][1]['metadata']['text']


def query_refiner(conversation, query):
    model = TextGenerationModel.from_pretrained("text-bison@001")
    response = model.predict(
    prompt=f"Dada a seguinte consulta do usuário e registro de conversa, formule uma pergunta que seria mais relevante para fornecer ao usuário uma resposta a partir de uma base de conhecimento.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:",
    temperature=0.2,
    max_output_tokens=256,
    top_p=0.5,
    top_k=20
    )
    return response.text


def get_conversation_history():
    conversation_string = ""
    for i in range(len(st.session_state['responses'])-1):
        
        conversation_string += "Human: "+st.session_state['requests'][i] + "\n"
        conversation_string += "Bot: "+ st.session_state['responses'][i+1] + "\n"
    return conversation_string