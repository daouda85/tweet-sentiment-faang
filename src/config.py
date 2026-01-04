class TwitterConfig:
    """Twitter API configuration - Mock version"""
    USE_MOCK_DATA: bool = True  # Set to True to use mock data
    
    # Mock search parameters
    SEARCH_QUERY: str = "artificial intelligence OR machine learning OR AI"
    MAX_TWEETS: int = 50
    LANGUAGE: str = "en"
    
    # Mock tweet data
    MOCK_TWEETS = [
        "AI is revolutionizing healthcare with new diagnostic tools! #ArtificialIntelligence",
        "Machine learning models are becoming more efficient every day.",
        "The future of technology depends on advancements in AI research.",
        "Natural language processing has improved significantly in recent years.",
        "I'm concerned about the ethical implications of artificial intelligence.",
        "Deep learning algorithms are achieving remarkable results.",
        "AI-powered chatbots are transforming customer service industries.",
        "The integration of AI in education shows promising results.",
        "Quantum computing will accelerate AI development exponentially.",
        "We need more regulation for responsible AI development."
    ]