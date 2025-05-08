import streamlit as st
from auth import authenticate_user
from fetcher import fetch_blogs
from analysis import analyze_blog
from mongodb import store_analysis, is_admin
from utils import generate_excel
from admin import admin_panel
from config import BLOG_SOURCES

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import time

st.set_page_config(page_title="Blog Analyzer", layout="wide")

# Login Handling
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h2 style='text-align:center;'>🔐 BlogAnalyzer Login</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("👤 Username")
            password = st.text_input("🔑 Password", type="password")
            login_btn = st.form_submit_button("🔓 Login")

            if login_btn:
                with st.spinner("Authenticating..."):
                    if authenticate_user(username, password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
    st.stop()

# Sidebar Source Selection
st.sidebar.title("📰 Select Blog Sources")
st.sidebar.markdown("Choose trusted blogs to analyze.")
selected_sources = st.sidebar.multiselect("✅ Blog Sites", list(BLOG_SOURCES.keys()))

# Admin Panel
if is_admin(st.session_state.username):
    st.sidebar.markdown("---")
    admin_panel()

# Main Layout Tabs
tab1, tab2 = st.tabs(["📊 Analyzer", "📁 Analysis Results"])

with tab1:
    st.title("📝 Blog Analyzer Dashboard")
    keyword = st.text_input("🔍 Enter a keyword for blog search")

    progress_bar = st.progress(0)
    status = st.empty()

    if st.button("🚀 Analyze"):
        status.info("⏳ Step 1: Fetching blogs...")
        blogs = fetch_blogs(keyword, selected_sources)
        progress_bar.progress(20)

        analyzed = []
        total = len(blogs)

        for i, blog in enumerate(blogs):
            status.info(f"⚙️ Step 2: Analyzing blog {i+1}/{total}...")
            blog["analysis"] = analyze_blog(blog)
            analyzed.append(blog)
            progress_bar.progress(20 + int((i + 1) / total * 60))

        store_analysis(keyword, st.session_state.username, analyzed)
        st.session_state.analyzed_blogs = analyzed

        progress_bar.progress(90)
        status.success(f"✅ Step 3: {len(analyzed)} blogs analyzed.")
        df_download = generate_excel(analyzed)
        st.download_button("📥 Download Excel Report", data=df_download, file_name=f"{keyword}_report.xlsx")

        for blog in analyzed:
            with st.expander(blog["title"]):
                st.markdown(f"**Website:** {blog['website']}")
                st.markdown(f"[🔗 Read More]({blog['link']})")
                st.markdown(f"**Published:** {blog['metadata'].get('published', 'N/A')}")
                st.markdown(f"**Content:** {blog['content']}")
                st.markdown(f"**🧠 VADER:** {blog['analysis']['vader']}")
                st.markdown(f"**💬 Empath:** {blog['analysis']['empath']}")
                st.markdown(f"**📚 LLM Summary:** {blog['analysis']['llm']}")

        progress_bar.progress(100)
        time.sleep(0.5)
        progress_bar.empty()
        status.empty()

with tab2:
    st.subheader("📊 Blog Sentiment Visualizations")
    if "analyzed_blogs" in st.session_state:
        data = []
        for blog in st.session_state.analyzed_blogs:
            data.append({
                "Title": blog["title"],
                "VADER Positive": blog["analysis"]["vader"]["pos"],
                "VADER Neutral": blog["analysis"]["vader"]["neu"],
                "VADER Negative": blog["analysis"]["vader"]["neg"],
                "Empath Positive": blog["analysis"]["empath"].get("positive_emotion", 0),
                "Empath Negative": blog["analysis"]["empath"].get("negative_emotion", 0),
            })

        df_chart = pd.DataFrame(data)

        if not df_chart.empty and "Title" in df_chart.columns:
            df_chart = df_chart.set_index("Title")
            st.bar_chart(df_chart[["VADER Positive", "VADER Neutral", "VADER Negative"]])

            pos_total = df_chart["Empath Positive"].sum()
            neg_total = df_chart["Empath Negative"].sum()
            pos_total = 0 if np.isnan(pos_total) else pos_total
            neg_total = 0 if np.isnan(neg_total) else neg_total

            if pos_total + neg_total > 0:
                fig, ax = plt.subplots()
                ax.pie([pos_total, neg_total],
                       labels=["Positive Emotion", "Negative Emotion"],
                       autopct='%1.1f%%', startangle=90)
                ax.axis("equal")
                st.pyplot(fig)
            else:
                st.warning("⚠️ No Empath emotion data available to display pie chart.")
        else:
            st.info("📭 No blog data available to visualize.")

        if st.button("🧹 Clear Analysis"):
            del st.session_state["analyzed_blogs"]
            st.success("✅ Analysis and charts cleared.")
            st.rerun()
    else:
        st.info("🔍 No analysis has been performed yet. Run a keyword query first.")