"""
Twitter Analyzer API
FastAPI backend for analyzing Twitter/X accounts
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import urllib3
from pathlib import Path

from twitter_client import TwitterAPIClient
from link_analyzer import LinkAnalyzer

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load .env from parent directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

app = FastAPI(
    title="Twitter Analyzer API",
    description="Analyze Twitter/X accounts and extract article links",
    version="1.0.0"
)

# CORS - Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
twitter_client = TwitterAPIClient()
link_analyzer = LinkAnalyzer()


class AnalyzeRequest(BaseModel):
    """Request model for /api/analyze endpoint"""
    username: str = Field(..., description="Twitter/X username (without @)")
    max_tweets: Optional[int] = Field(50, description="Number of tweets to fetch (5-100)", ge=5, le=100)
    analyze_links: Optional[bool] = Field(True, description="Whether to analyze article links")
    save_to_json: Optional[bool] = Field(False, description="Save results to JSON file")


class AnalyzeResponse(BaseModel):
    """Response model"""
    success: bool
    username: str
    user_info: Optional[dict] = None
    total_tweets: int
    tweets: list
    error: Optional[str] = None
    json_file_path: Optional[str] = None


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Twitter Analyzer API",
        "version": "1.0.0"
    }


@app.get("/api/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "twitter_api": "configured" if os.getenv('TWITTERAPI_IO_KEY') else "missing",
        "claude_api": "configured" if os.getenv('CLAUDE_API_KEY') else "missing"
    }


@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_user(request: AnalyzeRequest):
    """
    Analyze a Twitter/X user

    - **username**: Twitter username (without @)
    - **max_tweets**: Number of tweets to fetch (default: 50)
    - **analyze_links**: Whether to analyze article links (default: true)
    """
    try:
        # Fetch tweets
        print(f"Fetching tweets for @{request.username}...")
        result = twitter_client.get_user_tweets(
            username=request.username,
            max_results=request.max_tweets
        )

        if not result['success']:
            raise HTTPException(
                status_code=400,
                detail=result.get('error', 'Failed to fetch tweets')
            )

        tweets = result['tweets']

        # Analyze links if requested
        if request.analyze_links and tweets:
            print(f"Analyzing links in {len(tweets)} tweets...")
            tweets = link_analyzer.analyze_links(tweets)

        # Prepare response data
        response_data = {
            "success": True,
            "username": result['username'],
            "user_info": result.get('user_info'),
            "total_tweets": len(tweets),
            "tweets": tweets,
            "error": None,
            "json_file_path": None
        }

        # Save to JSON if requested
        if request.save_to_json:
            # Create exports directory if it doesn't exist
            exports_dir = Path(__file__).parent.parent / 'exports'
            exports_dir.mkdir(exist_ok=True)

            # Generate filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{request.username}_{timestamp}.json"
            filepath = exports_dir / filename

            # Save to JSON with pretty formatting
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(response_data, f, ensure_ascii=False, indent=2)

            response_data['json_file_path'] = str(filepath)
            print(f"Results saved to: {filepath}")

        return AnalyzeResponse(**response_data)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in analyze_user: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/api/test/{username}")
async def test_user_lookup(username: str):
    """Quick test endpoint to lookup a user"""
    user_info = twitter_client.get_user_info(username)

    if user_info:
        return {
            "success": True,
            "username": username,
            "user_info": user_info
        }
    else:
        return {
            "success": False,
            "username": username,
            "error": "User not found"
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
