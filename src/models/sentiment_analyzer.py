import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    pipeline
)
from typing import Dict, List, Any
import pandas as pd
from src.config import model_config
from src.utils.logger import project_logger

class SentimentAnalyzer:
    """Sentiment analysis model wrapper"""
    
    def __init__(self, model_name: str = None):
        self.logger = project_logger
        self.model_name = model_name or model_config.MODEL_NAME
        
        self.logger.info(f"Loading model: {self.model_name}")
        self._load_model()
        
    def _load_model(self):
        """Load model and tokenizer"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self.pipeline = pipeline(
                "sentiment-analysis",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if torch.cuda.is_available() else -1
            )
            self.logger.info("Model loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            raise
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of a single text"""
        try:
            result = self.pipeline(text[:model_config.MAX_LENGTH])[0]
            return {
                "label": result["label"],
                "score": float(result["score"]),
                "text": text[:200]  # Truncated for display
            }
        except Exception as e:
            self.logger.error(f"Error analyzing text: {e}")
            return {"label": "ERROR", "score": 0.0, "text": text[:200]}
    
    def analyze_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Analyze multiple texts in batch"""
        results = []
        for text in texts:
            results.append(self.analyze_text(text))
        return results
    
    def save_model(self, path: str = None):
        """Save model locally"""
        save_path = path or model_config.MODEL_PATH
        self.model.save_pretrained(save_path)
        self.tokenizer.save_pretrained(save_path)
        self.logger.info(f"Model saved to {save_path}")

# Singleton instance
sentiment_analyzer = SentimentAnalyzer()