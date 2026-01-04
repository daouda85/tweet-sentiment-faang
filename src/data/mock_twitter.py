import random
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict
import json

class MockTwitterData:
    """Generate realistic mock Twitter data for testing"""
    
    def __init__(self, num_tweets: int = 100):
        self.num_tweets = num_tweets
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
    
    def generate_tweet(self) -> Dict:
        """Generate a single mock tweet"""
        user = random.choice(self.users)
        topic = random.choice(self.topics)
        hashtag = random.choice(self.hashtags)
        
        tweets = [
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
        
        return {
            "id": str(random.randint(1000000000000000000, 9999999999999999999)),
            "text": random.choice(tweets),
            "created_at": created_at.isoformat(),
            "user": {
                "name": user,
                "screen_name": user.lower(),
                "followers_count": random.randint(100, 10000)
            },
            "retweet_count": random.randint(0, 500),
            "favorite_count": random.randint(0, 1000),
            "hashtags": [hashtag],
            "sentiment": random.choice(["positive", "neutral", "negative"])
        }
    
    def generate_tweets(self, num_tweets: int = None) -> List[Dict]:
        """Generate multiple mock tweets"""
        if num_tweets is None:
            num_tweets = self.num_tweets
        
        return [self.generate_tweet() for _ in range(num_tweets)]
    
    def to_dataframe(self, num_tweets: int = None) -> pd.DataFrame:
        """Convert mock tweets to pandas DataFrame"""
        tweets = self.generate_tweets(num_tweets)
        return pd.DataFrame(tweets)
    
    def save_to_json(self, filename: str = "mock_tweets.json"):
        """Save mock tweets to JSON file"""
        tweets = self.generate_tweets()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(tweets, f, indent=2, default=str)

# Usage example
if __name__ == "__main__":
    mock = MockTwitterData(num_tweets=50)
    df = mock.to_dataframe()
    print(f"Generated {len(df)} mock tweets")
    print(df.head())