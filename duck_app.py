from duckduckgo_search import DDGS
import streamlit as st

st.set_page_config(page_title="DuckDuckGo Search", page_icon="🦆")

ddgs = DDGS()

def search(query):
    return ddgs.text(query)

st.title("DuckDuckGo Search 🦆")
query = st.text_input("Enter your search query")

if query:
    results = search(query)
    for result in results:
        st.write("---")
        st.write(f"### [{result['title']}]({result['href']})")
        st.write(result['body'])