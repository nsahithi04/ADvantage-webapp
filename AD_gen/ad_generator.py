import sys
import os
import openai
import psycopg2
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def fetch_top_trends(limit=5):
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cursor = conn.cursor()

    cursor.execute("""
        SELECT topic, summary FROM google_trends_now
        ORDER BY scraped_date DESC, id ASC
        LIMIT %s;
    """, (limit,))

    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results



def generate_ads(product_name, product_description, trends):
    prompt = (
        f"You are a professional copywriter for an AI-powered advertising platform. "
        f"A client is selling a product named **{product_name}**.\n\n"
        f"Product Description: {product_description}\n\n"
        "Your job is to write **one short, engaging ad** for each of the following trending topics. "
        "Each ad should be catchy, creative, and subtly relate the trend to the product. Do not copy the trend summary. Be original but contextually relevant.\n\n"
    )

    for i, (topic, summary) in enumerate(trends, start=1):
        prompt += f"{i}. Trend: {topic}\nSummary: {summary}\nAd:"

    prompt += "\n\nGenerate all ads now, one for each trend."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You create short, trend-based ad copy tailored to specific products."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=600,
        temperature=0.85
    )

    # Parse the response into a list of ads
    ads = []
    ad_lines = response.choices[0].message.content.strip().split('\n')
    
    for i, line in enumerate(ad_lines):
        if i % 2 == 0:  # Trend line
            trend = line.replace("Trend: ", "")
        else:  # Ad content line
            ad_content = line.replace("Ad:", "").strip()
            ads.append({'trend': trend, 'ad_content': ad_content})

    return ads


if __name__ == "__main__":
    product_name = sys.argv[1]  # Get the product name from command line args
    product_description = sys.argv[2]  # Get the description from command line args
    trends = fetch_top_trends()  # Fetch top trends
    ads = generate_ads(product_name, product_description, trends)

    # Clean the ads to remove incomplete entries
# Clean the ads to remove incomplete entries
cleaned_ads = []
for ad in ads:
    trend = ad.get('trend', '').strip()
    content = ad.get('ad_content', '').strip()

    # Handle mix-ups: Swap if trend looks like content
    if len(trend) > 100 and len(content) < 50:
        trend, content = content, trend

    # Extra checks
    if trend.lower().startswith("ad for "):
        trend = trend.replace("Ad for ", "").strip()

    # Skip incomplete ads (either trend or content is missing)
    if not trend or not content:
        continue  # Skip this ad if it's incomplete

    # Print only the ad content (without the trend)
    print(content)
    
    cleaned_ads.append({'trend': trend, 'content': content})

# No need for final ad entry print
