import streamlit as st
import feedparser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from urllib.parse import quote
from datetime import datetime
from dateutil import parser as date_parser
import time
from zoneinfo import ZoneInfo

# Page configuration
st.set_page_config(
    page_title="Market Sentiment Analysis",
    page_icon="📊",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sentiment-box {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .positive-box {
        background-color: #d4edda;
        color: #155724;
        border: 2px solid #c3e6cb;
    }
    .neutral-box {
        background-color: #fff3cd;
        color: #856404;
        border: 2px solid #ffeaa7;
    }
    .negative-box {
        background-color: #f8d7da;
        color: #721c24;
        border: 2px solid #f5c6cb;
    }
    .source-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
        color: #2c3e50;
    }
    .stats-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_news(query, days_filter=7):
    """Fetch news from Google News RSS"""
    date_query = f"{query} when:{days_filter}d"
    rss_url = f"https://news.google.com/rss/search?q={quote(date_query)}"
    feed = feedparser.parse(rss_url)
    articles = []
    for item in feed.entries:
        articles.append({
            "title": item.title,
            "link": item.link,
            "published": item.get('published', 'N/A')
        })
    return articles

def analyze_sentiment(text):
    """Local VADER sentiment (no external calls)"""
    if not text or not text.strip():
        return 'Neutral'
    analyzer = SentimentIntensityAnalyzer()
    compound = analyzer.polarity_scores(text)['compound']
    if compound >= 0.05:
        return 'Positive'
    elif compound <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

def analyze_news_sentiment(stock_name, days_filter=7):
    """Fetch and group news by sentiment"""
    queries = [
        f"{stock_name} market", f"{stock_name} price", f"{stock_name} news",
        f"{stock_name} trends", f"{stock_name} analysis", f"{stock_name} forecast"
    ]
    
    all_articles = []
    seen = set()
    
    progress = st.progress(0)
    status = st.empty()
    
    for i, query in enumerate(queries):
        status.text(f"📰 Fetching: {query}")
        articles = fetch_news(query, days_filter)
        for a in articles:
            key = (a['title'], a['link'])
            if key not in seen:
                seen.add(key)
                all_articles.append(a)
        progress.progress((i + 1) / len(queries))
        time.sleep(0.1)
    
    status.text("🔍 Analyzing sentiment...")
    grouped = {"Positive": [], "Neutral": [], "Negative": []}
    for article in all_articles:
        sent = analyze_sentiment(article['title'])
        grouped[sent].append(article)
    
    progress.empty()
    status.empty()
    return grouped

# Main UI
st.markdown('<h1 class="main-header">📊 Market Sentiment Analysis</h1>', unsafe_allow_html=True)
st.markdown("""
    <p style='text-align: center; color: #666; margin-bottom: 2rem;'>
    Analyze market sentiment from news articles using local VADER sentiment analysis.
    </p>
""", unsafe_allow_html=True)

# Input
col1, col2 = st.columns([3, 1])
with col1:
    stock_name = st.text_input("Enter stock or company name:", placeholder="e.g., Apple, Tesla, Bitcoin")
with col2:
    days_filter = st.number_input("Days Range:", min_value=1, max_value=30, value=7, step=1)

# Analyze Button
if st.button("🔍 Analyze Sentiment", type="primary", use_container_width=True):
    if not stock_name.strip():
        st.warning("⚠️ Please enter a stock name.")
    else:
        with st.spinner("Analyzing news sentiment..."):
            grouped_articles = analyze_news_sentiment(stock_name.strip(), days_filter)
            total = sum(len(v) for v in grouped_articles.values())
            
            if total == 0:
                st.error("❌ No news articles found. Try a different name or increase days.")
            else:
                # Sentiment Overview
                st.markdown('<p class="source-header">📰 News Sentiment Overview</p>', unsafe_allow_html=True)
                pos_pct = len(grouped_articles["Positive"]) / total * 100
                neu_pct = len(grouped_articles["Neutral"]) / total * 100
                neg_pct = len(grouped_articles["Negative"]) / total * 100
                
                cols = st.columns(3)
                for col, (sent, perc) in zip(cols, [("Positive", pos_pct), ("Neutral", neu_pct), ("Negative", neg_pct)]):
                    emoji = "😊" if sent == "Positive" else "😐" if sent == "Neutral" else "😟"
                    box_class = "positive-box" if sent == "Positive" else "neutral-box" if sent == "Neutral" else "negative-box"
                    col.markdown(f"""
                        <div class="sentiment-box {box_class}">
                            {emoji} {sent}<br>
                            <span style="font-size: 2rem;">{perc:.1f}%</span>
                        </div>
                    """, unsafe_allow_html=True)

                # 📈 Detailed Statistics
                st.markdown("---")
                st.markdown("### 📈 Detailed Statistics")
                st.markdown(f"""
                <div class="stats-box">
                    <strong>📰 Article Counts by Sentiment</strong><br>
                    ✅ Positive Articles: <strong>{len(grouped_articles['Positive'])}</strong><br>
                    ⚪ Neutral Articles: <strong>{len(grouped_articles['Neutral'])}</strong><br>
                    ❌ Negative Articles: <strong>{len(grouped_articles['Negative'])}</strong><br>
                    <strong>Total Articles:</strong> {total}
                </div>
                """, unsafe_allow_html=True)

                                # === INTERACTIVE TABS WITH IST TIME ===
                st.markdown("---")
                st.subheader("📰 Browse Articles by Sentiment")

                def convert_to_ist(pub_str):
                    """Convert RSS published string (assumed GMT/UTC) to IST string"""
                    try:
                        # Parse the date (feedparser usually gives RFC-2822)
                        dt_utc = date_parser.parse(pub_str)
                        # Ensure it's timezone-aware as UTC
                        if dt_utc.tzinfo is None:
                            dt_utc = dt_utc.replace(tzinfo=ZoneInfo("UTC"))
                        # Convert to IST
                        dt_ist = dt_utc.astimezone(ZoneInfo("Asia/Kolkata"))
                        return dt_ist.strftime("%a, %d %b %Y %I:%M %p IST")
                    except Exception:
                        return pub_str  # fallback

                def parse_date_for_sort(article):
                    try:
                        return date_parser.parse(article.get('published', ''))
                    except:
                        return datetime.min

                pos_sorted = sorted(grouped_articles["Positive"], key=parse_date_for_sort, reverse=True)
                neu_sorted = sorted(grouped_articles["Neutral"], key=parse_date_for_sort, reverse=True)
                neg_sorted = sorted(grouped_articles["Negative"], key=parse_date_for_sort, reverse=True)

                tab1, tab2, tab3 = st.tabs([
                    f"✅ Positive Articles ({len(pos_sorted)})",
                    f"⚪ Neutral Articles ({len(neu_sorted)})",
                    f"❌ Negative Articles ({len(neg_sorted)})"
                ])

                with tab1:
                    if pos_sorted:
                        for i, a in enumerate(pos_sorted, 1):
                            ist_time = convert_to_ist(a['published'])
                            st.markdown(f"**{i}. [😊 {a['title']}]({a['link']})**")
                            st.caption(f"Published: {ist_time}")
                            st.markdown("---")
                    else:
                        st.info("No positive articles found.")

                with tab2:
                    if neu_sorted:
                        for i, a in enumerate(neu_sorted, 1):
                            ist_time = convert_to_ist(a['published'])
                            st.markdown(f"**{i}. [😐 {a['title']}]({a['link']})**")
                            st.caption(f"Published: {ist_time}")
                            st.markdown("---")
                    else:
                        st.info("No neutral articles found.")

                with tab3:
                    if neg_sorted:
                        for i, a in enumerate(neg_sorted, 1):
                            ist_time = convert_to_ist(a['published'])
                            st.markdown(f"**{i}. [😟 {a['title']}]({a['link']})**")
                            st.caption(f"Published: {ist_time}")
                            st.markdown("---")
                    else:
                        st.info("No negative articles found.")
# Footer
st.markdown("---")
st.markdown("""
    <p style='text-align: center; color: #999; font-size: 0.9rem;'>
    💡 <strong>Local News Sentiment Analyzer</strong><br>
    Uses VADER (rule-based, no external APIs). Results are for informational purposes only.<br>
    🔒 All processing happens in your browser session. No data is stored.
    </p>
""", unsafe_allow_html=True)