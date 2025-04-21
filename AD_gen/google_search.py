import time
from serpapi import GoogleSearch  # pip install google-search-results
from transformers import pipeline  # pip install transformers torch
from newspaper import Article  # pip install newspaper3k

# Replace with your valid SerpAPI key
SERPAPI_KEY = "cce95d8cb288c235f863c21cf383c166c07922af6e9268767188e8ded0ac6e68"

# Initialize the summarization model (using Facebook's BART-large-cnn)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def get_all_results_from_serpapi(query):
    """
    Uses SerpAPI to search Google for the given query and returns a list of organic results.
    """
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    print("DEBUG: Raw SERPAPI response:", results)  # Debug print to inspect response
    organic_results = results.get("organic_results", [])
    return organic_results

def aggregate_and_summarize(query):
    """
    Aggregates all snippets from the organic results and produces an overall summary.
    """
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results.get("organic_results", [])
    
    aggregated_text = " ".join(res.get("snippet", "") for res in organic_results if res.get("snippet"))
    overall_summary = summarize_text(aggregated_text)
    return overall_summary

def extract_article_text(url):
    """
    Uses Newspaper3k to extract full article text from the given URL.
    """
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"Error extracting article from {url}: {e}")
        return ""

def summarize_text(text):
    """
    Uses the summarization model to generate a summary of the provided text.
    """
    if len(text.strip()) == 0:
        return "No content available to summarize."
    try:
        trimmed_text = text[:3000]
        summary = summarizer(trimmed_text, max_length=100, min_length=50)
        return summary
    except Exception as e:
        return f"Summary error: {str(e)}"

def process_query(query):
    """
    Processes the query by retrieving search results, summarizing each result's snippet and full article,
    and then aggregating snippets for an overall summary.
    """
    results = get_all_results_from_serpapi(query)
    if not results:
        print("No organic search results found.")
        return

    aggregated_snippets = []
    for i, res in enumerate(results[:3], 1):  # Just top 3

        title = res.get("title", "N/A")
        link = res.get("link", "N/A")
        snippet = res.get("snippet", "")
        aggregated_snippets.append(snippet)
        
        print(f"{i}. Title: {title}")
        print(f"   Link: {link}")
        print(f"   Snippet: {snippet}")
        
        # Extract full article text and summarize it
        article_text = extract_article_text(link)
        if article_text:
            article_summary = summarize_text(article_text)
            print(f"   Full Article Summary: {article_summary}")
        else:
            print("   Could not extract full article text.")
        print("-" * 80)
    
    # Aggregate all snippets and generate an overall summary
    aggregated_text = " ".join(aggregated_snippets)
    overall_summary = summarize_text(aggregated_text)
    print("\nOverall Aggregated Summary:")
    print(overall_summary)

if __name__ == "__main__":
    query = input("Enter your query: ")
    process_query(query)
