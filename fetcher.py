import feedparser
from config import BLOG_SOURCES
from newspaper import Article
from googlesearch import search

TRUSTED_SOURCES = [
    "TechCrunch", "The Verge", "Wired", "Medium Health", "Medium Technology",
    "Reddit World News", "BBC News", "CNN Top Stories", "OpenAI Blog", "Medium Menopause Matters"
]

def fetch_from_url(url, keyword):
    try:
        article = Article(url)
        article.download()
        article.parse()
        content = article.text.strip()
        if keyword.lower() in content.lower():
            return {
                "title": article.title or url,
                "content": content,
                "link": url,
                "website": url.split('/')[2],
                "metadata": {
                    "published": "",
                    "author": article.authors[0] if article.authors else "Unknown",
                    "likes": 0
                }
            }
    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
    return None

def search_web(keyword, site="medium.com"):
    query = f"site:{site} {keyword}"
    return list(search(query, num_results=10))

def fetch_blogs(keyword, selected_sources=None):
    keyword_lower = keyword.lower()
    blogs = []

    # Step 1: RSS-Based Fetching
    if not selected_sources:
        selected_sources = TRUSTED_SOURCES

    for source in selected_sources:
        feed_url = BLOG_SOURCES.get(source)
        if not feed_url:
            continue

        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:10]:
                title = entry.get("title", "")
                summary = entry.get("summary", "")
                url = entry.get("link", "")
                try:
                    article = Article(url)
                    article.download()
                    article.parse()
                    content = article.text.strip()
                except:
                    content = f"{title} {summary}"
                if all(word in content.lower() for word in keyword_lower.split()):
                    blogs.append({
                        "title": title,
                        "content": content,
                        "link": url,
                        "website": source,
                        "metadata": {
                            "published": entry.get("published", ""),
                            "author": entry.get("author", "Unknown"),
                            "likes": 0
                        }
                    })
        except Exception as e:
            print(f"[RSS ERROR] {source}: {e}")

    # Step 2: Fallback Google Search (no API)
    if not blogs:
        print("🔍 No matches from RSS. Falling back to Google search...")
        urls = search_web(keyword)
        for url in urls:
            blog = fetch_from_url(url, keyword)
            if blog:
                blogs.append(blog)

    return blogs
