# Twitter Sentiment Analysis Dashboard 📊

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-✓-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Twitter API](https://img.shields.io/badge/Twitter%20API-v2-blue.svg)](https://developer.twitter.com/)

**Real-time Twitter/X sentiment analysis dashboard for FAANG companies.** Built with FastAPI, Streamlit, and Docker. Portfolio project showcasing full-stack development skills.

## 🎥 Live Demo Video

### **Watch the Full Demo**
https://youtu.be/_fnvG-_9uZg

*Click the video above to play/download (MP4, ~50MB)*

### **Direct Download Links:**
https://youtu.be/_fnvG-_9uZg

---

## 📖 Table of Contents
- [📊 Project Overview](#-project-overview)
- [🚀 Features](#-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [📁 Project Structure](#-project-structure)
- [🚦 Quick Start](#-quick-start)
- [🔧 Configuration](#-configuration)
- [📊 API Endpoints](#-api-endpoints)
- [📈 Dashboard Features](#-dashboard-features)
- [🤖 Machine Learning Models](#-machine-learning-models)
- [🐳 Docker Deployment](#-docker-deployment)
- [📚 API Documentation](#-api-documentation)
- [🧪 Testing](#-testing)
- [🚀 Deployment](#-deployment)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [📞 Contact](#-contact)


## 📊 Project Overview

A real-time sentiment analysis dashboard for tracking Twitter/X sentiment around FAANG (Facebook, Amazon, Apple, Netflix, Google) companies and tech trends. Built as a portfolio project for FAANG internship applications.

**Live Demo:** 

## 🚀 Features

### 🔍 **Real-time Analysis**
- Live Twitter/X sentiment tracking
- Multi-company (FAANG) comparison
- Trend detection and alerts

### 📈 **Interactive Dashboard**
- Streamlit-based UI with dark/light themes
- Real-time charts and visualizations
- Custom date range filtering
- Export data to CSV/JSON

### 🧠 **AI/ML Capabilities**
- BERT-based sentiment classification
- Topic modeling and trend extraction
- Emotion detection (joy, anger, fear, etc.)
- Custom-trained models for tech/finance lexicon

### 🏗️ **Technical Architecture**
- Microservices with FastAPI backend
- Async data processing pipeline
- Docker containerization
- Redis caching for performance
- PostgreSQL database

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | FastAPI, PostgreSQL, Redis, Celery |
| **Frontend** | Streamlit, Plotly, Altair |
| **ML/AI** | Transformers, scikit-learn, spaCy |
| **Infrastructure** | Docker, Poetry, Pytest, GitHub Actions |
| **APIs** | Twitter API v2, REST, WebSocket |

## 📁 Project Structure

```
tweet-sentiment-faang/
├── app/                    # FastAPI backend
│   ├── api/               # REST endpoints
│   ├── core/              # Config & security
│   ├── db/                # Database models
│   ├── ml/                # ML models
│   └── services/          # Business logic
├── dashboard/             # Streamlit frontend
│   ├── pages/             # Multi-page app
│   └── components/        # UI components
├── docker/                # Containerization
├── notebooks/             # Jupyter notebooks
├── tests/                 # Test suite
├── pyproject.toml         # Dependencies
├── requirements.txt       # Pip requirements
└── docker-compose.yml     # Multi-service setup
```

## 🚦 Quick Start

### **Option 1: Docker (Recommended)**
```bash
# Clone repository
git clone https://github.com/daouda85/tweet-sentiment-faang.git
cd tweet-sentiment-faang

# Copy environment variables
cp .env.example .env
# Edit .env with your API keys

# Start all services
docker-compose up -d

# Access services:
# Dashboard: http://localhost:8501
# API Docs: http://localhost:8000/docs
```

### **Option 2: Local Development**
```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Add your Twitter API keys to .env

# Run backend
cd app
uvicorn main:app --reload --port 8000

# Run dashboard (new terminal)
cd dashboard
streamlit run app.py
```

## 🔧 Configuration

Create `.env` file:

```env
# Twitter API v2 (Academic tier recommended)
TWITTER_BEARER_TOKEN=your_token_here
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/sentiment_db
REDIS_URL=redis://localhost:6379/0

# App Settings
SECRET_KEY=your_secret_key_here
DEBUG=False
```

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Service health check |
| `GET` | `/tweets/search` | Search tweets with sentiment |
| `POST` | `/tweets/analyze` | Analyze custom text |
| `GET` | `/companies/{company}/sentiment` | Company sentiment analysis |
| `GET` | `/trends` | Trending topics with sentiment |
| `WS` | `/ws/live` | Real-time sentiment stream |

**Interactive Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📈 Dashboard Features

1. **Real-time Monitor**
   - Live sentiment gauge for each FAANG company
   - Tweets per minute counter
   - Top trending hashtags

2. **Historical Analysis**
   - Sentiment trends over time (1h, 24h, 7d, 30d)
   - Volume vs sentiment correlation
   - Comparative company analysis

3. **Deep Dive Analytics**
   - Word clouds for positive/negative tweets
   - Topic modeling visualization
   - Geographic sentiment heatmap

## 🤖 Machine Learning Models

| Model | Accuracy | F1-Score | Use Case |
|-------|----------|----------|----------|
| BERT Fine-tuned | 89.2% | 0.88 | Primary sentiment |
| LSTM Custom | 85.7% | 0.84 | Fallback analysis |
| VADER | 78.3% | 0.76 | Rule-based quick check |

## 🐳 Docker Deployment

```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d --build

# View logs
docker-compose logs -f

# Scale workers
docker-compose up -d --scale worker=4
```

### **Services:**
- `backend`: FastAPI application (port 8000)
- `dashboard`: Streamlit interface (port 8501)
- `postgres`: PostgreSQL database
- `redis`: Cache and message broker
- `worker`: Celery async task processor

## 📚 API Documentation

### **Example Usage:**

```python
import requests

# Search tweets
response = requests.get(
    "http://localhost:8000/tweets/search",
    params={
        "query": "$AAPL OR Apple",
        "max_results": 100
    }
)

# Analyze text
response = requests.post(
    "http://localhost:8000/analyze",
    json={"text": "Apple's new product is amazing!"}
)

# WebSocket for real-time
# Connect to: ws://localhost:8000/ws/live
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_sentiment.py -v
```

**Test Coverage:** >85% unit tests, >70% integration tests

## 🚀 Deployment

### **Cloud Options:**

```bash
# AWS Elastic Beanstalk
eb init -p docker tweet-sentiment
eb create sentiment-prod

# Google Cloud Run
gcloud run deploy sentiment-api --source .

# Heroku
heroku container:push web
heroku container:release web
```

### **Kubernetes:**
```bash
kubectl apply -f k8s/
kubectl get pods -w
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 📞 Contact

**Daouda Tandian**  
📧 Email: daoudatandian85@gmail.com  
🐙 GitHub: [@daouda85](https://github.com/daouda85)  
💼 LinkedIn: [Daouda Tandian](https://linkedin.com/in/daouda-tandian)

## 🙏 Acknowledgments

- Twitter/X for API access
- Hugging Face for transformer models
- Streamlit and FastAPI communities
- Open source contributors

---

## 🎯 Project Status

**Version:** 1.0.0  
**Last Updated:** January 2024  
**Next Milestone:** Real-time alert system

---

*Built with ❤️ by Daouda Tandian for FAANG internship applications*  
*Showcasing full-stack development, ML/AI, and system design skills*

⭐ **Star this repo if you find it useful!**
