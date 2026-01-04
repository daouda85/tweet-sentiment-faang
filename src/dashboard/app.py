import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime
import time
import random

# ========== CONFIGURATION ==========
class DashboardConfig:
    HOST: str = "localhost"
    PORT: int = 8501
    TITLE: str = "Twitter Sentiment Analysis Dashboard - Daouda Tandian"

dashboard_config = DashboardConfig()

# ========== PAGE SETUP ==========
st.set_page_config(
    page_title=dashboard_config.TITLE,
    page_icon="🐦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1DA1F2;
        text-align: center;
        margin-bottom: 1rem;
    }
    .creator-credit {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .creator-credit strong {
        color: #1DA1F2;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .positive { color: #00C853; font-weight: bold; }
    .neutral { color: #FF9800; font-weight: bold; }
    .negative { color: #F44336; font-weight: bold; }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 5px 5px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1DA1F2;
        color: white;
    }
    .footer-note {
        text-align: center;
        color: #666;
        font-size: 0.9rem;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ========== SIDEBAR ==========
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/124/124021.png", width=80)
    st.title("⚙️ Dashboard Settings")
    
    # Creator info
    st.markdown("---")
    st.markdown("### 👨‍💻 Created by")
    st.markdown("**Daouda Tandian**")
    st.markdown("FAANG Internship Project")
    st.markdown("---")
    
    # API Configuration
    api_url = st.text_input("API Server URL", "http://localhost:8000")
    
    # Data Settings
    st.subheader("📊 Data Settings")
    tweet_limit = st.slider("Tweets to Display", 10, 100, 30)
    refresh_rate = st.slider("Auto-refresh (seconds)", 10, 300, 60)
    
    # Filter Options
    st.subheader("🔍 Filters")
    sentiment_filter = st.selectbox(
        "Sentiment Filter",
        ["All", "Positive", "Neutral", "Negative"]
    )
    
    # Actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh Now", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("📊 Test API", use_container_width=True):
            try:
                response = requests.get(f"{api_url}/api/health")
                if response.status_code == 200:
                    st.success("✅ API Connected!")
                else:
                    st.error("❌ API Connection Failed")
            except:
                st.error("❌ Cannot reach API")

# ========== HEADER ==========
st.markdown(f'<h1 class="main-header">🐦 Twitter Sentiment Analysis Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="creator-credit">Created by <strong>Daouda Tandian</strong> • FAANG Internship Project</p>', unsafe_allow_html=True)
st.caption(f"Real-time sentiment analysis powered by FastAPI • Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ========== DATA FETCHING ==========
@st.cache_data(ttl=30)  # Cache for 30 seconds
def fetch_data(api_url: str, limit: int = 30):
    """Fetch data from API"""
    try:
        # Fetch tweets
        tweets_response = requests.get(f"{api_url}/api/tweets?limit={limit}", timeout=5)
        tweets = tweets_response.json() if tweets_response.status_code == 200 else {"tweets": []}
        
        # Fetch trending data
        trending_response = requests.get(f"{api_url}/api/trending", timeout=5)
        trending = trending_response.json() if trending_response.status_code == 200 else {}
        
        return tweets.get("tweets", []), trending
    except Exception as e:
        st.error(f"⚠️ Error fetching data: {str(e)}")
        return [], {}

# Fetch data
tweets, trending = fetch_data(api_url, tweet_limit)

# Apply sentiment filter
if sentiment_filter != "All":
    tweets = [t for t in tweets if t.get('sentiment', '').lower() == sentiment_filter.lower()]

# ========== METRICS ROW ==========
st.subheader("📈 Key Metrics")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Total Tweets", len(tweets))
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    positive_tweets = sum(1 for t in tweets if t.get('sentiment') == 'positive')
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Positive", positive_tweets, 
              delta=f"{positive_tweets/len(tweets)*100:.1f}%" if tweets else "0%")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    neutral_tweets = sum(1 for t in tweets if t.get('sentiment') == 'neutral')
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Neutral", neutral_tweets,
              delta=f"{neutral_tweets/len(tweets)*100:.1f}%" if tweets else "0%")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    negative_tweets = sum(1 for t in tweets if t.get('sentiment') == 'negative')
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Negative", negative_tweets,
              delta=f"{negative_tweets/len(tweets)*100:.1f}%" if tweets else "0%")
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    avg_confidence = sum(t.get('confidence', 0) for t in tweets) / len(tweets) if tweets else 0
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Avg Confidence", f"{avg_confidence:.1%}")
    st.markdown('</div>', unsafe_allow_html=True)

# ========== MAIN CONTENT TABS ==========
tab1, tab2, tab3, tab4 = st.tabs(["📊 Sentiment Analysis", "📈 Trends", "🐦 Recent Tweets", "🔍 Analyze Text"])

# Tab 1: Sentiment Analysis
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        if tweets:
            # Sentiment distribution pie chart
            sentiment_counts = pd.DataFrame({
                'Sentiment': ['Positive', 'Neutral', 'Negative'],
                'Count': [positive_tweets, neutral_tweets, negative_tweets]
            })
            
            fig_pie = px.pie(
                sentiment_counts,
                values='Count',
                names='Sentiment',
                title='Sentiment Distribution',
                color='Sentiment',
                color_discrete_map={
                    'Positive': '#00C853',
                    'Neutral': '#FF9800',
                    'Negative': '#F44336'
                },
                hole=0.3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No tweet data available. Make sure the API server is running.")
    
    with col2:
        if tweets:
            # Sentiment over time (simulated)
            st.subheader("Sentiment Timeline")
            
            # Create timeline data
            timeline_data = []
            for i in range(10):
                hour_ago = datetime.now() - pd.Timedelta(hours=9-i)
                timeline_data.append({
                    'Hour': hour_ago.strftime('%H:00'),
                    'Positive': random.randint(20, 40),
                    'Neutral': random.randint(15, 30),
                    'Negative': random.randint(5, 20)
                })
            
            timeline_df = pd.DataFrame(timeline_data)
            
            fig_timeline = go.Figure()
            fig_timeline.add_trace(go.Scatter(
                x=timeline_df['Hour'], y=timeline_df['Positive'],
                name='Positive', line=dict(color='#00C853', width=3)
            ))
            fig_timeline.add_trace(go.Scatter(
                x=timeline_df['Hour'], y=timeline_df['Neutral'],
                name='Neutral', line=dict(color='#FF9800', width=3)
            ))
            fig_timeline.add_trace(go.Scatter(
                x=timeline_df['Hour'], y=timeline_df['Negative'],
                name='Negative', line=dict(color='#F44336', width=3)
            ))
            
            fig_timeline.update_layout(
                title='Sentiment Trends (Last 10 Hours)',
                xaxis_title='Time',
                yaxis_title='Number of Tweets',
                hovermode='x unified'
            )
            st.plotly_chart(fig_timeline, use_container_width=True)

# Tab 2: Trends
with tab2:
    st.subheader("📈 Trends & Analytics")
    
    # Check if we have data
    if not trending:
        trending = {
            'trending_topics': [
                {'topic': 'Artificial Intelligence', 'count': 45},
                {'topic': 'Machine Learning', 'count': 38},
                {'topic': 'Data Science', 'count': 32},
                {'topic': 'AI Ethics', 'count': 27},
                {'topic': 'Deep Learning', 'count': 23}
            ],
            'sentiment_distribution': {'positive': 45, 'neutral': 35, 'negative': 20}
        }
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Always show topics chart
        topics_data = trending.get('trending_topics', [])
        if topics_data:
            topics_df = pd.DataFrame(topics_data)
            fig = px.bar(
                topics_df,
                x='topic',
                y='count',
                title='🔥 Trending Topics',
                color='count',
                text='count'
            )
            fig.update_traces(textposition='outside')
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No trending topics data")
    
    with col2:
        # Always show sentiment chart
        sentiment_data = trending.get('sentiment_distribution', {'positive': 45, 'neutral': 35, 'negative': 20})
        
        # Convert to DataFrame
        sentiment_list = []
        for sentiment, count in sentiment_data.items():
            sentiment_list.append({
                'Sentiment': sentiment.capitalize(),
                'Count': count
            })
        
        sentiment_df = pd.DataFrame(sentiment_list)
        
        fig2 = px.pie(
            sentiment_df,
            values='Count',
            names='Sentiment',
            title='📊 Sentiment Distribution',
            color='Sentiment',
            color_discrete_map={
                'Positive': '#00C853',
                'Neutral': '#FF9800',
                'Negative': '#F44336'
            },
            hole=0.3
        )
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Show summary
    st.divider()
    st.subheader("📊 Summary - Daouda Tandian")
    
    total_tweets = sum(sentiment_data.values())
    col_sum1, col_sum2, col_sum3 = st.columns(3)
    
    with col_sum1:
        st.metric("Positive", f"{sentiment_data.get('positive', 0)}", 
                 f"{sentiment_data.get('positive', 0)/total_tweets*100:.1f}%")
    
    with col_sum2:
        st.metric("Neutral", f"{sentiment_data.get('neutral', 0)}", 
                 f"{sentiment_data.get('neutral', 0)/total_tweets*100:.1f}%")
    
    with col_sum3:
        st.metric("Negative", f"{sentiment_data.get('negative', 0)}", 
                 f"{sentiment_data.get('negative', 0)/total_tweets*100:.1f}%")

# Tab 3: Recent Tweets
with tab3:
    if tweets:
        st.subheader(f"📝 Recent Tweets ({len(tweets)} total)")
        
        # Search and filter
        search_query = st.text_input("🔍 Search tweets...", placeholder="Type keywords to filter")
        
        filtered_tweets = tweets
        if search_query:
            filtered_tweets = [t for t in tweets if search_query.lower() in t.get('text', '').lower()]
        
        # Display tweets
        for i, tweet in enumerate(filtered_tweets[:20]):
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    # User info
                    user = tweet.get('user', {})
                    st.markdown(f"**👤 {user.get('name', 'Unknown')}** (@{user.get('screen_name', 'user')})")
                    
                    # Tweet text
                    tweet_text = tweet.get('text', '')
                    st.write(tweet_text)
                    
                    # Hashtags
                    hashtags = tweet.get('hashtags', [])
                    if hashtags:
                        hashtag_str = " ".join(hashtags)
                        st.caption(f"Tags: {hashtag_str}")
                    
                    # Metadata
                    col_meta1, col_meta2, col_meta3 = st.columns(3)
                    with col_meta1:
                        st.caption(f"🔄 {tweet.get('retweet_count', 0)}")
                    with col_meta2:
                        st.caption(f"❤️ {tweet.get('favorite_count', 0)}")
                    with col_meta3:
                        created = tweet.get('created_at', '')
                        if created:
                            try:
                                dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                                st.caption(dt.strftime("%b %d, %H:%M"))
                            except:
                                st.caption(created[:16])
                
                with col2:
                    # Sentiment badge
                    sentiment = tweet.get('sentiment', 'neutral')
                    confidence = tweet.get('confidence', 0)
                    
                    if sentiment == 'positive':
                        st.markdown('<p class="positive">👍 POSITIVE</p>', unsafe_allow_html=True)
                    elif sentiment == 'negative':
                        st.markdown('<p class="negative">👎 NEGATIVE</p>', unsafe_allow_html=True)
                    else:
                        st.markdown('<p class="neutral">😐 NEUTRAL</p>', unsafe_allow_html=True)
                    
                    st.caption(f"{confidence:.0%} confidence")
                
                st.divider()
    else:
        st.info("No tweets to display. Start the API server to see tweets.")

# Tab 4: Analyze Text
with tab4:
    st.subheader("🔬 Custom Text Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        default_texts = [
            "I absolutely love how AI is transforming healthcare! This is amazing progress. #AI #Healthcare",
            "The new machine learning model shows concerning biases that need to be addressed immediately.",
            "Tech conference today discussed neural networks and their applications in various industries."
        ]
        
        selected_text = st.selectbox(
            "Choose a sample text or write your own:",
            default_texts + ["Custom..."]
        )
        
        if selected_text == "Custom...":
            text_to_analyze = st.text_area(
                "Enter your own text:",
                "I'm excited about the future of artificial intelligence and its potential benefits!",
                height=100
            )
        else:
            text_to_analyze = selected_text
            st.text_area("Text to analyze:", text_to_analyze, height=100)
    
    with col2:
        st.markdown("### How it works")
        st.markdown("""
        1. Enter any text in the box
        2. Click 'Analyze Sentiment'
        3. Get instant sentiment analysis
        4. View confidence score
        """)
        st.info("Powered by FastAPI & ML models • Daouda Tandian")

    # Add creator credit below the analyze button
    st.markdown("---")
    st.markdown("#### 🚀 Project Highlights")
    st.markdown("""
    - **Real-time sentiment analysis** using transformer models
    - **Full-stack architecture** (FastAPI + Streamlit)
    - **Production-ready** with Docker & CI/CD
    - **Interactive visualization** with Plotly
    - **Mock data generation** for demo purposes
    """)
    
    if st.button("🎯 Analyze Sentiment", type="primary", use_container_width=True):
        with st.spinner("Analyzing sentiment..."):
            try:
                response = requests.post(
                    f"{api_url}/api/analyze",
                    data={"text": text_to_analyze}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display results
                    st.success("✅ Analysis Complete!")
                    
                    col_res1, col_res2, col_res3 = st.columns(3)
                    
                    with col_res1:
                        sentiment = result['sentiment']
                        if sentiment == 'positive':
                            st.markdown('<h2 class="positive">👍 POSITIVE</h2>', unsafe_allow_html=True)
                        elif sentiment == 'negative':
                            st.markdown('<h2 class="negative">👎 NEGATIVE</h2>', unsafe_allow_html=True)
                        else:
                            st.markdown('<h2 class="neutral">😐 NEUTRAL</h2>', unsafe_allow_html=True)
                    
                    with col_res2:
                        st.metric("Confidence", f"{result['confidence']*100:.1f}%")
                    
                    with col_res3:
                        st.metric("Words", result['word_count'])
                    
                    # Confidence gauge
                    fig_gauge = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=result['confidence'] * 100,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "Confidence Level"},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': "#1DA1F2"},
                            'steps': [
                                {'range': [0, 50], 'color': "#F44336"},
                                {'range': [50, 75], 'color': "#FF9800"},
                                {'range': [75, 100], 'color': "#00C853"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 90
                            }
                        }
                    ))
                    
                    fig_gauge.update_layout(height=300)
                    st.plotly_chart(fig_gauge, use_container_width=True)
                    
                    # Hashtags found
                    if result.get('hashtags'):
                        st.markdown("**📌 Hashtags detected:**")
                        for tag in result['hashtags']:
                            st.markdown(f"`{tag}`", unsafe_allow_html=True)
                    
                    # Add creator signature to results
                    st.markdown("---")
                    st.markdown("*Analysis performed by Daouda Tandian's Sentiment Analysis System*")
                else:
                    st.error("❌ Failed to analyze text. API error.")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Make sure the API server is running at " + api_url)

# ========== FOOTER ==========
st.divider()
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.caption("🔄 Auto-refreshing in " + str(refresh_rate) + "s")

with footer_col2:
    if st.button("Clear Cache"):
        st.cache_data.clear()
        st.rerun()

with footer_col3:
    st.caption("Dashboard v1.0 • Created by Daouda Tandian")

# Final footer with full credit
st.markdown("---")
st.markdown("""
<div class="footer-note">
    <h4>📋 Project Information</h4>
    <p><strong>Twitter Sentiment Analysis Dashboard</strong></p>
    <p>Created by: <strong>Daouda Tandian</strong></p>
    <p>FAANG Internship Project • Full-Stack ML Application</p>
    <p>Technologies: Python, FastAPI, Streamlit, Plotly, Docker</p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh
time.sleep(refresh_rate)
st.rerun()