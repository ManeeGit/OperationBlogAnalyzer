# blog_analyzer/config.py

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")

BLOG_SOURCES = {
    # 🌐 World & News
    "BBC News": "http://feeds.bbci.co.uk/news/rss.xml",
    "CNN Top Stories": "http://rss.cnn.com/rss/cnn_topstories.rss",
    "NYTimes World": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",

    # 🧠 AI & Technology
    "TechCrunch": "https://techcrunch.com/feed/",
    "The Verge": "https://www.theverge.com/rss/index.xml",
    "Wired": "https://www.wired.com/feed/rss",
    "Ars Technica": "http://feeds.arstechnica.com/arstechnica/index",
    "OpenAI Blog": "https://openai.com/blog/rss.xml",
    "Google AI Blog": "https://ai.googleblog.com/feeds/posts/default",
    "Microsoft AI Blog": "https://blogs.microsoft.com/ai/feed/",
    "NVIDIA Blog": "https://blogs.nvidia.com/blog/feed/",

    # 🧬 Health & Wellness
    "Medium Health": "https://medium.com/feed/tag/health",
    "Medium Women": "https://medium.com/feed/tag/women",
    "Medium Wellness": "https://medium.com/feed/tag/wellness",
    "Medium Menopause": "https://medium.com/feed/tag/menopause",
    "Medium Menopause Matters": "https://medium.com/feed/menopause-matters-empowering-womens-health",

    # 🕰️ History & Society
    "Medium History": "https://medium.com/feed/tag/history",
    "Medium Politics": "https://medium.com/feed/tag/politics",
    "Smithsonian Magazine": "https://www.smithsonianmag.com/rss/",
    "History.com": "https://www.history.com/.rss",

    # 🔐 Cybersecurity
    "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
    "Dark Reading": "https://www.darkreading.com/rss.xml",
    "Bleeping Computer": "https://www.bleepingcomputer.com/feed/",

    # 👥 Reddit Communities
    "Reddit AI": "https://www.reddit.com/r/artificial/.rss",
    "Reddit Health": "https://www.reddit.com/r/health/.rss",
    "Reddit World News": "https://www.reddit.com/r/worldnews/.rss",
    "Reddit History": "https://www.reddit.com/r/history/.rss",
    "Reddit Technology": "https://www.reddit.com/r/technology/.rss",

    # 📖 Medium Topics
    "Medium AI": "https://medium.com/feed/tag/artificial-intelligence",
    "Medium Technology": "https://medium.com/feed/tag/technology",
    "Medium Science": "https://medium.com/feed/tag/science",
    "Medium World": "https://medium.com/feed/tag/world",

    # 🔬 Research & Science
    "Science Daily": "https://www.sciencedaily.com/rss/all.xml",
    "National Geographic": "https://www.nationalgeographic.com/content/natgeo/en_us/index.rss"
}
