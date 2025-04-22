import os
import openai
from dotenv import load_dotenv

load_dotenv()

client = os.getenv("OPENAI_API_KEY")

def summarize_trend(trend_name, search_summary):
    prompt = (
        f"You are a smart news assistant. Your job is to summarize what '{trend_name}' is about "
        "based on recent search results. Focus on clarity, context, and why this is trending.\n\n"
        f"Search Results:\n{search_summary}\n\n"
        "Summary:"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes news and web search results."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error during summarization: {str(e)}"
