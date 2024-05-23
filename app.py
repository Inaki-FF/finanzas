import streamlit as st
import pickle

st.title("Financial Analysis Query App")

# Load secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Load the query engine from the pickle file
with open("query_engine.pkl", "rb") as f:
    s_engine = pickle.load(f)

query = st.text_area("Enter your query here", height=200)
if st.button("Run Query"):
    with st.spinner("Processing..."):
        response = s_engine.query(query)
    st.markdown(response)
