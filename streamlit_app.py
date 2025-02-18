import os, json
import requests
import streamlit as st

# Get the API key from environment variables
SERP_API_KEY = os.getenv("SERP_API_KEY")

def web_search(query):
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERP_API_KEY,
        "engine": "google"
    }
    response = requests.get(url, params=params)
    results = response.json()
    return results

def load_data():
    with open("response.json", "r") as f:
        return json.load(f)

def main():
    st.title("Search Results 🔎")
    
    # Get query input from the user.
    query = st.text_input("Enter your search query", "latest news in AI")
    
    if query:
        # st.info("Fetching results from SerpAPI...")
        # data = web_search(query)
        data = load_data()
        
        with st.sidebar:
            # --- Display Search Metadata ---
            if "search_metadata" in data:
                st.header("Search Metadata")
                st.json(data.get("search_metadata", {}))
            
            # --- Display Search Parameters ---
            if "search_parameters" in data:
                st.header("Search Parameters")
                st.json(data.get("search_parameters", {}))
            
            # --- Display Search Information ---
            if "search_information" in data:
                st.header("Search Information")
                st.json(data.get("search_information", {}))
            
        # --- Related Questions ---
        if st.checkbox("Show related questions"):
            if "related_questions" in data:
                st.header("Related Questions")
                for item in data.get("related_questions", []):
                    st.subheader(item.get("question", ""))
                    if item.get("snippet"):
                        st.write(item.get("snippet"))
                    st.markdown(f"[Read more]({item.get('link', '#')})")
                    if item.get("thumbnail"):
                        st.image(item.get("thumbnail"), width=100)
                    st.markdown("---")
        
        # --- Organic Results ---
        if "organic_results" in data:
            st.header("Organic Results")
            for result in data.get("organic_results", []):
                st.subheader(result.get("title", ""))
                st.write(result.get("snippet", ""))
                st.markdown(f"[Visit site]({result.get('link', '#')})")
                if result.get("favicon"):
                    st.image(result.get("favicon"), width=30)
                # Display sitelinks if available
                sitelinks = result.get("sitelinks", {}).get("inline", [])
                if sitelinks:
                    st.write("Sitelinks:")
                    for link in sitelinks:
                        st.markdown(f"- [{link.get('title')}]({link.get('link')})")
                st.markdown("---")
        
        # --- Perspectives (if available) ---
        if "perspectives" in data:
            st.header("Perspectives")
            for perspective in data.get("perspectives", []):
                st.subheader(perspective.get("title", ""))
                st.write(f"Author: {perspective.get('author', '')} | Source: {perspective.get('source', '')} | Date: {perspective.get('date', '')}")
                st.markdown(f"[View]({perspective.get('link', '#')})")
                thumbnails = perspective.get("thumbnails", [])
                if thumbnails:
                    st.image(thumbnails[0], width=150)
                st.markdown("---")
        
        # --- Top Stories (if available) ---
        if "top_stories" in data:
            st.header("Top Stories")
            for story in data.get("top_stories", []):
                st.subheader(story.get("title", ""))
                st.write(f"Source: {story.get('source', '')} | Date: {story.get('date', '')}")
                st.markdown(f"[Read more]({story.get('link', '#')})")
                if story.get("thumbnail"):
                    st.image(story.get("thumbnail"), width=150)
                st.markdown("---")
        
        # --- Related Searches ---
        if "related_searches" in data:
            st.header("Related Searches")
            for search in data.get("related_searches", []):
                st.markdown(f"- [{search.get('query', '')}]({search.get('link', '#')})")
        
        # --- Pagination Info ---
        if "pagination" in data:
            st.header("Pagination")
            pagination = data.get("pagination", {})
            st.write("Current Page:", pagination.get("current"))
            st.markdown(f"[Next Page]({pagination.get('next', '#')})")
    else:
        st.write("Enter a query above to fetch results.")

if __name__ == "__main__":
    main()
