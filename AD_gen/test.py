from trend_fetcher import fetch_trends_from_db
from trend_research_agent import google_search
from trend_summarizer_agent import summarize_trend

# Fetch top 5 current trends
trends = fetch_trends_from_db(table_name="google_trends_now", limit=5)

for trend in trends:
    print(f"\n🔎 Searching: {trend}")
    search_results = google_search(trend)
    
    print(f"🧠 Summarizing: {trend}")
    summary = summarize_trend(trend, search_results)
    
    print(f"📝 Final Summary for '{trend}':\n{summary}\n{'-'*60}")
