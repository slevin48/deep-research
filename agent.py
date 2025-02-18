#%%
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os, json
import openai
import requests

load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")
# %%
# Step 1: Web Search 
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

# # %%
# from duckduckgo_search import DDGS
# ddgs = DDGS()
# ddgs.text("latest news in AI")

# %%
# Example usage:
results = web_search("latest news in AI")
results
# %%
# Save the results to a JSON file
with open("response.json", "w") as f:
    f.write(json.dumps(results, indent=4))
# %%
# Load the results from the JSON file
with open("response.json", "r") as f:
    results = json.load(f)
# %%
# Extract and return the top result snippets
snippets = [item["snippet"] for item in results.get("organic_results", [])]
for i, result in enumerate(snippets):
    print(f"Result {i+1}: {result}")
# %%
# Step 2: Robust Content Extraction

def extract(html):
    # try:
    #     document = readability.Document(html)
    #     return document.summary()
    # except:
    soup = BeautifulSoup(html, "html.parser")
    # return ' '.join([p.get_text() for p in soup.select('p')][:10])
    return soup.get_text()

#%%
# Example usage:
html = requests.get(results["organic_results"][0]["link"]).text
content = extract(html)
content
# %%
# Save the content to a text file
with open("content2.txt", "w", encoding="utf-8") as f:
    f.write(content)
# %%
#  Step 3: AI agent reasoning over the content to generate a report
def agent(research):
    completion = openai.chat.completions.create(
        model="o3-mini",
        messages=[
            {"role": "developer", "content": "You are a helpful research assistant."},
            {"role": "user", "content": research}
        ]
    )
    return completion.choices[0].message.content
# %%
query = "What is the latest news in AI?"
prompt = f"""
{query}
Answer based on the web search results:
{content}
"""
report = agent(prompt)
report
# %% 
# Save the report to a text file
with open("report.txt", "w", encoding="utf-8") as f:
    f.write(report)