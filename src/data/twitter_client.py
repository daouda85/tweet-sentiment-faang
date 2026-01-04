import tweepy
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd
from src.config import twitter_config
from src.models.sentiment_analyzer import sentiment_analyzer
from src.utils.logger import project_logger

class TwitterClient:
    """Twitter API client with sentiment analysis"""
    
    def __init__(self):
        self.logger = project_logger
        self.client = None
        self._authenticate()
        
    def _authenticate(self):
        """Authenticate with Twitter API"""
        try:
            twitter_config.validate()
            
            self.client = tweepy.Client(
                bearer_token=twitter_config.BEARER_TOKEN,
                consumer_key=twitter_config.API_KEY,
                consumer_secret=twitter_config.API_SECRET,
                access_token=twitter_config.ACCESS_TOKEN,
                access_token_secret=twitter_config.ACCESS_SECRET,
                wait_on_rate_limit=True
            )
            
            self.logger.info("Twitter API authenticated successfully")
        except Exception as e:
            self.logger.error(f"Twitter authentication failed: {e}")
            raise
    
    def search_tweets(
        self,
        query: str = None,
        max_results: int = 10,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Search tweets and analyze sentiment"""
        try:
            query = query or twitter_config.SEARCH_QUERY
            max_results = min(max_results, twitter_config.MAX_TWEETS)
            
            self.logger.info(f"Searching tweets: {query}")
            
            # Search tweets
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=[
                    'created_at',
                    'public_metrics',
                    'author_id',
                    'lang'
                ],
                expansions=['author_id'],
                **kwargs
            )
            
            if not tweets.data:
                self.logger.warning("No tweets found")
                return []
            
            # Process tweets
            processed_tweets = []
            for tweet in tweets.data:
                if tweet.lang != twitter_config.LANGUAGE:
                    continue
                    
                sentiment_result = sentiment_analyzer.analyze_text(tweet.text)
                
                tweet_data = {
                    "id": str(tweet.id),
                    "text": tweet.text[:500],  # Truncate for storage
                    "author_id": str(tweet.author_id),
                    "created_at": tweet.created_at.isoformat() if tweet.created_at else None,
                    "retweets": tweet.public_metrics["retweet_count"],
                    "likes": tweet.public_metrics["like_count"],
                    "replies": tweet.public_metrics["reply_count"],
                    "sentiment": sentiment_result["label"],
                    "confidence": sentiment_result["score"],
                    "query": query,
                    "collected_at": datetime.now().isoformat()
                }
                
                processed_tweets.append(tweet_data)
                self.logger.debug(f"Tweet analyzed: {sentiment_result['label']}")
            
            self.logger.info(f"Processed {len(processed_tweets)} tweets")
            return processed_tweets
            
        except Exception as e:
            self.logger.error(f"Error searching tweets: {e}")
            return []
    
    def save_to_csv(self, tweets: List[Dict], filename: str = None):
        """Save tweets to CSV file"""
        if not tweets:
            return None
        
        df = pd.DataFrame(tweets)
        if filename:
            filepath = Path(__file__).parent.parent.parent / "data" / filename
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = Path(__file__).parent.parent.parent / "data" / f"tweets_{timestamp}.csv"
        
        df.to_csv(filepath, index=False, encoding='utf-8')
        self.logger.info(f"Saved {len(df)} tweets to {filepath}")
        return filepath

# Singleton instance
twitter_client = TwitterClient()