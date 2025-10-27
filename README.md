# 📊 Market Sentiment Analysis – Local News Analyzer

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-teal?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)
![Local Processing](https://img.shields.io/badge/Privacy-Local%20Only-ff69b4)

A **privacy-first**, **zero-API**, **client-side** Streamlit app that analyzes market sentiment from Google News articles using **VADER sentiment analysis** — all processed locally in your browser session.  
Published timestamps are automatically converted from **GMT (UTC)** to **Indian Standard Time (IST)** for user convenience.

---

## 🌟 Features

- 🔍 **Real-time News Fetching**: Pulls recent news (last 1–30 days) from Google News RSS.
- 🧠 **Local Sentiment Analysis**: Uses **VADER** (Valence Aware Dictionary for sEntiment Reasoning) — no external APIs, no data leaves your machine.
- 🕒 **Timezone Conversion**: Automatically converts article publish times from **GMT/UTC → IST (Asia/Kolkata)**.
- 📈 **Visual Sentiment Dashboard**: 
  - Color-coded sentiment percentages (Positive / Neutral / Negative)
  - Article counts & statistics
  - Interactive tabs to browse articles by sentiment
- 🔒 **Privacy Guaranteed**: 
  - No user data stored
  - No tracking
  - All processing happens in your Streamlit session
- 📱 **Responsive UI**: Clean, modern design optimized for desktop and mobile.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher (required for `zoneinfo`)
- `pip` package manager

### Installation

1. **Clone or download** this repository:
   ```bash
   git clone https://github.com/your-username/market-sentiment-analyzer.git
   cd market-sentiment-analyzer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**:
   ```bash
   streamlit run app.py
   ```

4. Open your browser to `http://localhost:8501` and start analyzing!

---

## 📦 Dependencies (`requirements.txt`)

```txt
streamlit>=1.30.0
feedparser>=6.0.0
vaderSentiment>=3.3.2
python-dateutil>=2.8.0
```

> ✅ **No internet APIs** are called during sentiment analysis — VADER runs entirely offline.

---

## 🌍 Timezone Handling

Google News RSS feeds publish timestamps in **GMT (UTC)**. This app:

1. Parses the published date string (e.g., `"Mon, 27 Oct 2025 10:30:00 GMT"`)
2. Treats it as **UTC** if no timezone info is present
3. Converts it to **IST (UTC+5:30)** using Python’s built-in `zoneinfo` module
4. Displays it as:  
   `Mon, 27 Oct 2025 04:00 PM IST`

> 💡 **Note**: Requires **Python 3.9+** for `zoneinfo`. For older versions, install `backports.zoneinfo`.

---

## 🛡️ Privacy & Security

- 🔐 **Zero data collection**: No cookies, no analytics, no logging.
- 🌐 **No external API calls** during sentiment analysis — VADER is rule-based and runs locally.
- 📁 **No persistent storage**: All data is discarded when you close the browser tab.
- 🧪 **Safe for sensitive queries**: Analyze stocks like `Reliance`, `Tata Motors`, or even `Bitcoin` without exposing your interests.

> ⚠️ **Disclaimer**: Results are for **informational purposes only** and should not be used as financial advice.

---

## 🖼️ Screenshots

### Dashboard Overview
![Sentiment Dashboard](screenshots/dashboard.png)

### Article Tabs with IST Timestamps
![IST Time Display](screenshots/ist-time.png)

---

## 🛠️ Customization

You can easily extend or modify the app:

| Feature | How to Customize |
|--------|------------------|
| **Default days range** | Change `value=7` in `st.number_input()` |
| **Sentiment thresholds** | Modify `compound >= 0.05` logic in `analyze_sentiment()` |
| **News sources** | Replace Google News RSS URL with another feed |
| **UI colors** | Edit `.positive-box`, `.neutral-box`, etc. in `<style>` block |
| **Supported timezones** | Change `"Asia/Kolkata"` to any [IANA timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) |

---

## 🐛 Troubleshooting

### ❌ `ModuleNotFoundError: No module named 'zoneinfo'`
- **Cause**: Using Python < 3.9
- **Fix**:
  ```bash
  pip install backports.zoneinfo
  ```
  Then replace the import in `app.py`:
  ```python
  try:
      from zoneinfo import ZoneInfo
  except ImportError:
      from backports.zoneinfo import ZoneInfo
  ```

### ❌ "No news articles found"
- Try a more common stock name (e.g., `Apple` instead of `AAPL`)
- Increase the **Days Range** to 14 or 30
- Ensure you have internet access (RSS fetching requires it)

### ❌ Slow loading
- Google News may throttle requests — the app uses caching (`@st.cache_data(ttl=1800)`) to reduce repeated calls.
- Wait ~10–15 seconds for full analysis.

---

## 📜 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

> You are free to use, modify, and distribute this code — even commercially — with proper attribution.

---

## 🙌 Acknowledgements

- **[VADER Sentiment](https://github.com/cjhutto/vaderSentiment)** by C.J. Hutto
- **[Streamlit](https://streamlit.io/)** for the amazing open-source framework
- **[Google News RSS](https://news.google.com/rss)** for free, accessible news feeds
- **[Python `zoneinfo`](https://docs.python.org/3/library/zoneinfo.html)** for robust timezone support

---

## 📬 Feedback & Contributions

Found a bug? Have an idea?  
👉 Open an [Issue](https://github.com/your-username/market-sentiment-analyzer/issues) or submit a [Pull Request](https://github.com/your-username/market-sentiment-analyzer/pulls)!

---

> 💡 **Pro Tip**: Deploy this app on [Streamlit Community Cloud](https://streamlit.io/cloud) for free — just link your GitHub repo!

---

**Happy Analyzing!** 📈😊  
*Made with ❤️ for traders, investors, and curious minds in India and beyond.*# Market_-Sentiment_Analysis
# Market_-Sentiment_Analysis
# Market_Sentiment_Analysis
