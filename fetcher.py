import feedparser
from config import BLOG_SOURCES

def fetch_blogs(keyword, selected_sources=None):
    blogs = []
    sources = selected_sources or BLOG_SOURCES.keys()
    for name in sources:
        feed_url = BLOG_SOURCES[name]
        parsed = feedparser.parse(feed_url)
        for entry in parsed.entries:
            if keyword.lower() in entry.title.lower() or keyword.lower() in getattr(entry, "summary", "").lower():
                blogs.append({
                    "website": name,
                    "title": entry.title,
                    "link": entry.link,
                    "content": entry.summary,
                    "metadata": {
                        "published": entry.get("published", "N/A")
                    }
                })
    return blogs
