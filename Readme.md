# Facebook Insights Microservice 📊

This microservice scrapes Facebook page data (e.g., basic details, posts, followers) and stores it in a MongoDB database. It exposes RESTful APIs to query and retrieve insights about Facebook pages. Additionally, it offers AI-powered summaries using Google's Gemini Palm model (optional).

---

## Table of Contents 📑
- [Features](#features)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
- [Bonus Features](#bonus-features)

---

## Features ✨

### Core Features
- **Scrape Facebook Pages**: Extracts detailed information about a Facebook page, including name, profile picture, follower count, likes, posts, and more.
- **Store Data in MongoDB**: Organizes scraped data into structured schemas for efficient querying.
- **Expose RESTful APIs**: Provides endpoints to fetch page details, list pages, and retrieve recent posts.
- **Pagination Support**: Implements pagination for endpoints returning large datasets.
- **Caching**: Uses Redis for caching API responses with a TTL (Time To Live) of 5 minutes to reduce redundant queries and improve performance.

### Bonus Features 🎁
- **AI-Powered Summaries**: Generates concise summaries of a Facebook page using Google's Gemini Palm model.
- **Asynchronous Programming**: Supports asynchronous tasks for scraping and database operations to handle high I/O workloads.
- **Storage Server Integration**: Uploads profile pictures and media to AWS S3 or Google Cloud Storage (GCS) for persistent storage.

---

## Requirements 📦

### Prerequisites
- Python 3.8+
- MongoDB (local or cloud instance)
- Redis (for caching)
- Google Gemini API Key (optional, for AI-powered summaries)

### Dependencies
Install the required libraries by running:

```bash
pip install -r requirements.txt
```

---

## Setup Instructions 🚀

### Step 1: Clone the Repository
```bash
git clone https://github.com/AneeshRijhwani25/facebook-insights.git
cd facebook-insights
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Create a `.env` file in the root directory and add the following variables:

```env
MONGO_URI=mongodb://localhost:27017/facebook_insights
CACHE_TYPE=redis
CACHE_REDIS_URL=redis://localhost:6379/0
GEMINI_API_KEY=your_gemini_api_key_here
```

### Step 4: Start MongoDB and Redis
Ensure MongoDB and Redis are running locally:

```bash
mongod
redis-server
```

### Step 5: Run the Application
Start the Flask application:

```bash
python run.py
```

The application will be available at [http://localhost:5000](http://localhost:5000).

---

## API Documentation 📡

### Base URL
All endpoints are prefixed with `/api`.

### Endpoints

#### 1. Fetch Page Details
`GET /api/page/{username}`

Fetches details of a specific Facebook page by username. If the page is not cached or stored in the database, it scrapes the data in real-time.

**Response Example:**
```json
{
  "username": "boat.lifestyle",
  "name": "Boat Lifestyle",
  "url": "https://www.facebook.com/boat.lifestyle",
  "profile_pic": "https://example.com/profile.jpg",
  "follower_count": 120000,
  "likes_count": 150000,
  "category": "Lifestyle",
  "posts": [
    {
      "content": "Check out our new collection!",
      "created_at": "2023-10-01T12:00:00Z",
      "likes_count": 5000,
      "comments": []
    }
  ]
}
```

#### 2. List Pages
`GET /api/pages`

Lists all pages stored in the database with optional filters.

**Query Parameters:**
- `follower_range`: Filter pages by follower count range (e.g., `20000-40000`).
- `category`: Filter pages by category (e.g., `Business`).
- `page`: Pagination page number (default: 1).
- `limit`: Number of results per page (default: 10).

**Response Example:**
```json
{
  "total": 10,
  "results": [
    {
      "username": "boat.lifestyle",
      "name": "Boat Lifestyle",
      "follower_count": 120000
    }
  ]
}
```

#### 3. Get Recent Posts
`GET /api/posts/{username}`

Retrieves the 10 most recent posts of a Facebook page.

**Response Example:**
```json
[
  {
    "content": "Check out our new collection!",
    "created_at": "2023-10-01T12:00:00Z",
    "likes_count": 5000,
    "comments": []
  }
]
```

#### 4. Generate AI Summary (Bonus)
`GET /api/summary/{username}`

Generates an AI-powered summary of a Facebook page using Google's Gemini Palm model.

**Response Example:**
```json
{
  "username": "boat.lifestyle",
  "summary": "Boat Lifestyle is a popular lifestyle brand with over 120k followers. Their content focuses on fashion and accessories."
}
```

---

## Bonus Features 🎉

### Asynchronous Scraping
The scraper uses asynchronous programming to handle I/O-bound tasks like web scraping and database operations efficiently, reducing delays and enhancing performance.

### Media Storage
Profile pictures and post media are uploaded to AWS S3 or Google Cloud Storage (GCS) for persistent storage. You can customize the storage logic by editing the file `app/utils.py` to integrate your preferred storage provider.

### Caching with Redis
Redis is used to cache API responses, reducing redundant database queries and improving overall response time.

