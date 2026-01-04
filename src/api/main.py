from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from datetime import datetime, timedelta
import uvicorn
import random
from typing import List, Dict, Any
import json

# ========== CONFIGURATION (No imports needed) ==========
class APIConfig:
    """API configuration"""
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    CORS_ORIGINS: list = ["http://localhost:8501", "http://127.0.0.1:8501"]

class TwitterConfig:
    """Twitter configuration (using mock data)"""
    USE_MOCK_DATA: bool = True
    SEARCH_QUERY: str = "artificial intelligence OR machine learning OR AI"
    MAX_TWEETS: int = 100
    LANGUAGE: str = "en"

# Create config instances
api_config = APIConfig()
twitter_config = TwitterConfig()

# ========== MOCK DATA GENERATOR ==========
class MockTwitterData:
    """Generate realistic mock Twitter data"""
    
    def __init__(self):
        self.users = [
            "TechEnthusiast42", "AIAnalyst", "DataSciencePro", "FutureTechWatch",
            "MLResearcher", "AIEthicist", "StartupFounder", "TechJournalist",
            "AcademicResearcher", "IndustryExpert"
        ]
        
        self.hashtags = [
            "#ArtificialIntelligence", "#MachineLearning", "#AI", "#DeepLearning",
            "#DataScience", "#Tech", "#Innovation", "#FutureTech", "#NLP", "#Robotics"
        ]
        
        self.topics = [
            "AI in healthcare", "Machine learning algorithms", "Natural language processing",
            "Computer vision", "Robotics", "AI ethics", "Quantum computing",
            "Neural networks", "Big data", "Automation"
        ]
    
    def generate_tweet(self, tweet_id: int) -> Dict:
        """Generate a single mock tweet"""
        user = random.choice(self.users)
        topic = random.choice(self.topics)
        hashtag = random.choice(self.hashtags)
        
        tweet_templates = [
            f"Exciting developments in {topic} recently! {hashtag}",
            f"New research paper on {topic} shows promising results. {hashtag}",
            f"Discussion: What are the ethical implications of {topic}? {hashtag}",
            f"Just attended a great conference about {topic}. Amazing insights! {hashtag}",
            f"Industry leaders are investing heavily in {topic}. {hashtag}",
            f"Concerns about {topic} need to be addressed by policymakers. {hashtag}",
            f"Breakthrough in {topic} could change everything. {hashtag}",
            f"My thoughts on the future of {topic}. {hashtag}",
            f"Recent advancements in {topic} are impressive. {hashtag}",
            f"How will {topic} impact our daily lives? {hashtag}"
        ]
        
        # Generate random date within last 7 days
        days_ago = random.randint(0, 7)
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        
        created_at = datetime.now() - timedelta(
            days=days_ago, 
            hours=hours_ago, 
            minutes=minutes_ago
        )
        
        # Generate sentiment with realistic distribution
        sentiment_roll = random.random()
        if sentiment_roll < 0.45:  # 45% positive
            sentiment = "positive"
            confidence = round(random.uniform(0.75, 0.98), 2)
        elif sentiment_roll < 0.8:  # 35% neutral
            sentiment = "neutral"
            confidence = round(random.uniform(0.7, 0.9), 2)
        else:  # 20% negative
            sentiment = "negative"
            confidence = round(random.uniform(0.75, 0.95), 2)
        
        return {
            "id": str(tweet_id),
            "text": random.choice(tweet_templates),
            "created_at": created_at.isoformat(),
            "user": {
                "name": user,
                "screen_name": user.lower(),
                "followers_count": random.randint(100, 10000)
            },
            "retweet_count": random.randint(0, 500),
            "favorite_count": random.randint(0, 1000),
            "hashtags": [hashtag],
            "sentiment": sentiment,
            "confidence": confidence,
            "source": "mock_data"
        }
    
    def generate_tweets(self, count: int = 50) -> List[Dict]:
        """Generate multiple mock tweets"""
        return [self.generate_tweet(i) for i in range(1000, 1000 + count)]

# Initialize mock data generator
mock_generator = MockTwitterData()

# ========== FASTAPI APP ==========
app = FastAPI(
    title="Twitter Sentiment Analysis API",
    description="Real-time sentiment analysis for FAANG internship project",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=api_config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== API ENDPOINTS ==========
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Twitter Sentiment Analysis API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/api/health",
            "tweets": "/api/tweets",
            "analyze": "/api/analyze",
            "trending": "/api/trending",
            "stats": "/api/stats"
        }
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "twitter-sentiment-api",
        "version": "1.0.0"
    }

@app.get("/api/tweets")
async def get_tweets(
    limit: int = 20,
    sentiment: str = None,
    start_date: str = None,
    end_date: str = None
):
    """
    Get tweets with sentiment analysis
    - limit: Number of tweets to return (default: 20, max: 100)
    - sentiment: Filter by sentiment (positive, neutral, negative)
    - start_date: Filter tweets after this date (ISO format)
    - end_date: Filter tweets before this date (ISO format)
    """
    # Validate limit
    if limit > 100:
        limit = 100
    
    # Generate mock tweets
    tweets = mock_generator.generate_tweets(limit)
    
    # Apply filters if provided
    if sentiment:
        tweets = [t for t in tweets if t["sentiment"] == sentiment.lower()]
    
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            tweets = [t for t in tweets if datetime.fromisoformat(t["created_at"]) >= start_dt]
        except:
            pass
    
    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            tweets = [t for t in tweets if datetime.fromisoformat(t["created_at"]) <= end_dt]
        except:
            pass
    
    return {
        "count": len(tweets),
        "tweets": tweets,
        "query": twitter_config.SEARCH_QUERY,
        "generated_at": datetime.now().isoformat()
    }

@app.post("/api/analyze")
async def analyze_text(text: str):
    """
    Analyze sentiment of a given text
    - text: The text to analyze
    """
    if not text or len(text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # Mock sentiment analysis (in real app, use ML model)
    words = text.lower().split()
    
    # Simple keyword-based sentiment (for demo)
    positive_words = ["good", "great", "excellent", "amazing", "love", "best", "positive", "happy"]
    negative_words = ["bad", "terrible", "worst", "hate", "negative", "sad", "awful", "problem"]
    
    positive_count = sum(1 for word in words if word in positive_words)
    negative_count = sum(1 for word in words if word in negative_words)
    
    if positive_count > negative_count:
        sentiment = "positive"
        confidence = round(random.uniform(0.7, 0.95), 2)
    elif negative_count > positive_count:
        sentiment = "negative"
        confidence = round(random.uniform(0.7, 0.95), 2)
    else:
        sentiment = "neutral"
        confidence = round(random.uniform(0.6, 0.85), 2)
    
    # Detect hashtags
    hashtags = [word for word in words if word.startswith("#")]
    
    return {
        "text": text,
        "sentiment": sentiment,
        "confidence": confidence,
        "hashtags": hashtags,
        "word_count": len(words),
        "analyzed_at": datetime.now().isoformat(),
        "model": "mock_sentiment_analyzer_v1"
    }

@app.get("/api/trending")
async def get_trending():
    """Get trending topics and sentiment distribution"""
    
    # Generate trending topics
    topics = [
        {"topic": "Artificial Intelligence", "count": random.randint(30, 60)},
        {"topic": "Machine Learning", "count": random.randint(25, 55)},
        {"topic": "Data Science", "count": random.randint(20, 50)},
        {"topic": "AI Ethics", "count": random.randint(15, 40)},
        {"topic": "Deep Learning", "count": random.randint(10, 35)},
        {"topic": "Neural Networks", "count": random.randint(8, 30)},
        {"topic": "Natural Language Processing", "count": random.randint(5, 25)},
        {"topic": "Computer Vision", "count": random.randint(5, 20)},
        {"topic": "Quantum Computing", "count": random.randint(3, 15)},
        {"topic": "Robotics", "count": random.randint(3, 15)}
    ]
    
    # Sort by count (descending)
    topics.sort(key=lambda x: x["count"], reverse=True)
    
    # Sentiment distribution
    sentiment_distribution = {
        "positive": random.randint(40, 60),
        "neutral": random.randint(25, 45),
        "negative": random.randint(10, 30)
    }
    
    total = sum(sentiment_distribution.values())
    
    return {
        "trending_topics": topics[:5],  # Top 5
        "sentiment_distribution": sentiment_distribution,
        "sentiment_percentages": {
            "positive": round(sentiment_distribution["positive"] / total * 100, 1),
            "neutral": round(sentiment_distribution["neutral"] / total * 100, 1),
            "negative": round(sentiment_distribution["negative"] / total * 100, 1)
        },
        "total_tweets_analyzed": random.randint(1000, 10000),
        "time_period": "last 24 hours",
        "generated_at": datetime.now().isoformat()
    }

@app.get("/api/stats")
async def get_stats():
    """Get API usage statistics"""
    return {
        "total_requests": random.randint(100, 1000),
        "tweets_analyzed": random.randint(500, 5000),
        "average_response_time_ms": round(random.uniform(50, 200), 2),
        "uptime": "99.8%",
        "active_since": (datetime.now() - timedelta(days=7)).isoformat(),
        "endpoints": {
            "health": "/api/health",
            "tweets": "/api/tweets",
            "analyze": "/api/analyze",
            "trending": "/api/trending",
            "stats": "/api/stats"
        }
    }

@app.get("/api/tweets/{tweet_id}")
async def get_tweet_by_id(tweet_id: str):
    """Get a specific tweet by ID"""
    # For demo, generate a tweet with the given ID
    tweet = mock_generator.generate_tweet(int(tweet_id) if tweet_id.isdigit() else 9999)
    tweet["id"] = tweet_id  # Use the requested ID
    
    return {
        "tweet": tweet,
        "requested_id": tweet_id,
        "found": True
    }

# ========== ERROR HANDLERS ==========
@app.exception_handler(404)
async def not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": f"Endpoint {request.url.path} not found", "error": "Not Found"}
    )

@app.exception_handler(500)
async def internal_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error", "error": "Internal Server Error"}
    )

# ========== START SERVER ==========
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=api_config.HOST,
        port=api_config.PORT,
        reload=api_config.DEBUG
    )