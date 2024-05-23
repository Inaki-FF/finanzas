import streamlit as st
import os
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.response.pprint_utils import pprint_response
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.query_engine import SubQuestionQueryEngine
import openai

# Set API keys
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit title
st.title("Financial Data Query App")

# User input for the query
query = st.text_area("Enter your query:")

if st.button("Submit Query"):

    acciones = SimpleDirectoryReader(input_files=["./files/Acciones.pdf"]).load_data()
    bonos = SimpleDirectoryReader(input_files=["./files/Bonos.pdf"]).load_data()
    mate_fin_1 = SimpleDirectoryReader(input_files=["./files/Matemáticas Financieras Parte 1.pdf"]).load_data()
    mate_fin_2 = SimpleDirectoryReader(input_files=["./files/Matemáticas Financieras Parte 2.pdf"]).load_data()
    mate_fin_4 = SimpleDirectoryReader(input_files=["./files/Matemáticas Financieras Parte 4.pdf"]).load_data()
    mate_fin_5 = SimpleDirectoryReader(input_files=["./files/Matemáticas Financieras Parte 5.pdf"]).load_data()
    valuación = SimpleDirectoryReader(input_files=["./files/Valuación de Empresas DCF-MúltiplosFF.pdf"]).load_data()

    acciones_index = VectorStoreIndex.from_documents(acciones)
    bonos_index = VectorStoreIndex.from_documents(bonos)
    mate_fin_1_index = VectorStoreIndex.from_documents(mate_fin_1)
    mate_fin_2_index = VectorStoreIndex.from_documents(mate_fin_2)
    mate_fin_4_index = VectorStoreIndex.from_documents(mate_fin_4)
    mate_fin_5_index = VectorStoreIndex.from_documents(mate_fin_5)
    valuación_index = VectorStoreIndex.from_documents(valuación)

    acciones_engine = acciones_index.as_query_engine(similarity_top_k=3)
    bonos_engine = bonos_index.as_query_engine(similarity_top_k=3)
    mate_fin_1_engine = mate_fin_1_index.as_query_engine(similarity_top_k=3)
    mate_fin_2_engine = mate_fin_2_index.as_query_engine(similarity_top_k=3)
    mate_fin_4_engine = mate_fin_4_index.as_query_engine(similarity_top_k=3)
    mate_fin_5_engine = mate_fin_5_index.as_query_engine(similarity_top_k=3)
    valuación_engine = valuación_index.as_query_engine(similarity_top_k=3)

    query_engine_tools = [
        QueryEngineTool(
            query_engine=acciones_engine,
            metadata=ToolMetadata(name="acciones", description="Provides information about Actions"),
        ),
        QueryEngineTool(
            query_engine=bonos_engine,
            metadata=ToolMetadata(name="bonos", description="Provides information about Bonds"),
        ),
        QueryEngineTool(
            query_engine=mate_fin_1_engine,
            metadata=ToolMetadata(name="mate_fin_1", description="Provides information about Financial Mathematics Part 1"),
        ),
        QueryEngineTool(
            query_engine=mate_fin_2_engine,
            metadata=ToolMetadata(name="mate_fin_2", description="Provides information about Financial Mathematics Part 2"),
        ),
        QueryEngineTool(
            query_engine=mate_fin_4_engine,
            metadata=ToolMetadata(name="mate_fin_4", description="Provides information about Financial Mathematics Part 4"),
        ),
        QueryEngineTool(
            query_engine=mate_fin_5_engine,
            metadata=ToolMetadata(name="mate_fin_5", description="Provides information about Financial Mathematics Part 5"),
        ),
        QueryEngineTool(
            query_engine=valuación_engine,
            metadata=ToolMetadata(name="valuación", description="Provides information about Company Valuation DCF-MúltiplosFF"),
        ),
    ]

    s_engine = SubQuestionQueryEngine.from_defaults(query_engine_tools=query_engine_tools)

    response = s_engine.query(query)
    
    # Display the response
    st.markdown(pprint_response(response))


