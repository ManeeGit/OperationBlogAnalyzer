import re
import feedparser
from config import BLOG_SOURCES

def fetch_blogs(keyword, selected_sources):
    if not selected_sources:
        selected_sources = list(BLOG_SOURCES.keys())

    keywords = keyword.lower().split()
    keyword_pattern = re.compile(r'\b(' + '|'.join(re.escape(k) for k in keywords) + r')\b', re.IGNORECASE)

    blogs = []

    for source in selected_sources:
        feed_url = BLOG_SOURCES[source]
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            link = entry.get("link", "")
            published = entry.get("published", "")

            # Check if any of the keywords appear in the title or summary
            if keyword_pattern.search(title) or keyword_pattern.search(summary):
                blogs.append({
                    "title": title,
                    "content": summary,
                    "link": link,
                    "website": source,
                    "metadata": {
                        "published": published,
                        "author": entry.get("author", "Unknown"),
                        "likes": 0  # Optional placeholder
                    }
                })

    return blogs
