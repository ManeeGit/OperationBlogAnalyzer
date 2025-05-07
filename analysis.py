# blog_analyzer/analysis.py

from openai import OpenAI
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from empath import Empath
from config import OPENAI_API_KEY

vader = SentimentIntensityAnalyzer()
empath = Empath()
client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_blog(blog):
    content = blog.get("content", "").strip()

    # VADER
    vader_result = vader.polarity_scores(content)

    # Empath
    empath_result = empath.analyze(content, categories=["positive_emotion", "negative_emotion"], normalize=True)

    # LLM (OpenAI GPT)
    if not content:
        llm_summary = "Content is empty. Skipping LLM analysis."
    else:
        try:
            print("Sending content to OpenAI (first 200 chars):", content[:200])
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Summarize the sentiment and intent of this blog:\n{content}"}],
                max_tokens=150
            )
            llm_summary = response.choices[0].message.content.strip()
        except Exception as e:
            print("OpenAI error:", e)
            llm_summary = f"LLM Error: {str(e)}"

    return {
        "vader": vader_result,
        "empath": empath_result,
        "llm": llm_summary
    }