# Deep Research Agent Tutorial

In this tutorial you’ll build an agent that combines a reasoning model (for example, an “o3‑mini‑high” style model), a web search API (using SERP or Google Custom Search), and web scraping to gather, process, and summarize information. (See the discussion on search & question answering in Chapter 4 of the book "Programming GPTs".)

─────────────────────────────  
**Tutorial Overview (60 minutes)**

1. **Introduction & Objectives (5 minutes)**
   - Explain what a deep research agent is: a system that reasons over a question, fetches real‑time data via web search, scrapes relevant webpages, and synthesizes an answer.
   - Outline the components:
     - A reasoning module (using a model similar to o3‑mini‑high)
     - A web search API integration
     - A web scraping component
   - Mention that you will “chain” these operations—concepts drawn from Chapter 4 (search & question answering) of the book "Programming GPTs".

2. **Environment Setup (10 minutes)**
   - **Prerequisites:** Python 3.8+ installed.
   - **Create a virtual environment:**
     ```
     python -m venv env
     env\Scripts\activate  # Windows (or source env/bin/activate on macOS/Linux)
     ```
   - **Install necessary packages:**
     ```
     pip install openai requests beautifulsoup4 langchain
     ```
     *(You may also install a SERP API client or use Google Custom Search’s client library.)*
   - Briefly review how these packages will help:
     - **openai / langchain:** for chaining and reasoning.
     - **requests & beautifulsoup4:** for fetching and parsing webpage content.

3. **Building the Reasoning Module (15 minutes)**
   - **Objective:** Create a function that uses your reasoning model.
   - **Code Example:**
     ```python
     import openai

     # Set your API key securely (e.g., from environment variables)
     openai.api_key = "YOUR_OPENAI_API_KEY"

     def reason(prompt, reasoning_effort="medium"):
         # In practice, replace the model name with your deployed reasoning model.
         messages = [{"role": "developer", "content": "You are a research assistant."},
          {"role": "user", "content": prompt}]
         response = openai.chat.completions.create(
             model="o3-mini",
             messages=messages,
             reasoning_effort=reasoning_effort
         )
         return response.choices[0].message.content.strip()

     # Example usage:
     question = "What are the latest news in AI?"
     reasoning_output = reason(f"Analyze the following research query and provide key points: {question}")
     print("Reasoning Output:", reasoning_output)
     ```
   - **Discussion:** Emphasize prompt engineering and chaining—the idea of feeding the initial query into the reasoning model to create a structured request for further search (a key concept from Chapter 3 and 4 of "Programming GPTs").

4. **Integrating the Web Search API (10 minutes)**
   - **Objective:** Query a web search API to get up‑to‑date information.
   - **Example using a SERP API (pseudo‑code):**
     ```python
     import requests

     SERP_API_KEY = "YOUR_SERP_API_KEY"
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

     # Example usage:
     search_results = web_search("latest news in AI")
     print("Search Results:", search_results)
     ```
   - **Discussion:** Explain that this call provides real‑time data that will later be fed into the chain. (This approach is similar to how Chapter 3 and Chapter 4 combine search results with reasoning in "Programming GPTs".)

5. **Implementing Web Scraping (10 minutes)**
   - **Objective:** Given a URL (from your search results), scrape its main content.
   - **Code Example:**
     ```python
     import requests
     from bs4 import BeautifulSoup

     def scrape_page(url):
         try:
             response = requests.get(url)
             response.raise_for_status()
             soup = BeautifulSoup(response.text, "html.parser")
             # Extract the page title and text content
             title = soup.title.string if soup.title else "No Title"
             paragraphs = soup.find_all("p")
             content = "\n".join([p.get_text() for p in paragraphs])
             return title, content
         except Exception as e:
             return None, f"Error scraping page: {e}"

     # Example usage:
     test_url = "https://example.com/some-research-article"
     title, content = scrape_page(test_url)
     print("Scraped Title:", title)
     print("Scraped Content Preview:", content[:200])
     ```
   - **Discussion:** Mention that this function can be integrated into your research agent to gather raw data that the reasoning module will later refine. (See similar scraping techniques in the book’s section on “Traditional Search” .)

6. **Chaining It All Together (10 minutes)**
   - **Objective:** Combine reasoning, search, and scraping into a unified workflow.
   - **Code Example:**
     ```python
     def research_agent(query):
         # Step 1: Reason over the query to create a structured search query.
         structured_query = reason(f"Rephrase this research question for a search query: {query}", reasoning_effort="low")
         
         # Step 2: Use the web search API to get relevant URLs/snippets.
         search_results = web_search(structured_query)
         print("Structured Query:", structured_query)
         print("Search Results:", search_results)
         
         # Step 3: For demonstration, take the first URL from search (assuming snippet includes a URL).
         # In practice, you might extract URLs from the API result.
         # For this example, we simulate with a hard-coded URL.
         url = "https://example.com/relevant-article"
         title, scraped_content = scrape_page(url)
         
         # Step 4: Use the reasoning module to summarize the scraped content.
         summary = reason(f"Summarize the following content briefly:\nTitle: {title}\nContent: {scraped_content[:1000]}", reasoning_effort="high")
         return summary

     # Example usage:
     final_answer = research_agent("What are the latest news in AI?")
     print("Final Answer:", final_answer)
     ```
   - **Discussion:** Explain how the output of one function feeds into the next—a key idea behind chaining that is central to the deep research agent design, as outlined in Chapter 3 (prompting, chaining, summarization) of "Programming GPTs".

7. **Wrap-Up & Further Enhancements (5 minutes)**
   - Recap what you built:
     - A reasoning module that re‑frames questions.
     - A web search function to retrieve live data.
     - A web scraping function to extract detailed content.
     - A chain that passes outputs from one step to the next.
   - Discuss potential enhancements:
     - Use error handling and logging.
     - Expand the scraping logic to handle multiple URLs.
     - Incorporate vector search for more in‑depth retrieval (as mentioned in later chapters of "Programming GPTs").
   - Suggest exploring frameworks like LangChain for more robust chaining and tool integration, as described in the book.

