"""
Twitter API Client using twitterapi.io
"""
import requests
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from parent directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class TwitterAPIClient:
    """Client for twitterapi.io API"""

    def __init__(self):
        self.api_key = os.getenv('TWITTERAPI_IO_KEY')
        self.base_url = "https://api.twitterapi.io"

        if not self.api_key:
            raise ValueError("TWITTERAPI_IO_KEY not found in environment")

    def get_user_info(self, username: str) -> Optional[Dict]:
        """Get user information"""
        url = f"{self.base_url}/twitter/user/info"
        headers = {"x-api-key": self.api_key}
        params = {"userName": username}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=15, verify=False)

            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return data.get('data', {})

            print(f"Error getting user info: {response.status_code}")
            print(f"Response: {response.text}")
            return None

        except Exception as e:
            print(f"Exception getting user info: {e}")
            return None

    def get_user_tweets(self, username: str, max_results: int = 50) -> Dict:
        """
        Get latest tweets from a user

        Args:
            username: Twitter username (without @)
            max_results: Number of tweets to fetch (default 50)

        Returns:
            Dict with user info and tweets
        """
        # Get user info first
        user_info = self.get_user_info(username)
        if not user_info:
            return {
                "success": False,
                "error": "User not found or API error",
                "username": username
            }

        # Get tweets - twitterapi.io returns ~20 tweets per request
        url = f"{self.base_url}/twitter/user/last_tweets"
        headers = {"x-api-key": self.api_key}

        all_tweets = []
        cursor = None
        requests_made = 0
        max_requests = (max_results // 20) + 1  # Calculate needed requests

        print(f"[INFO] Fetching up to {max_results} tweets (estimated {max_requests} API requests needed)")

        try:
            while len(all_tweets) < max_results and requests_made < max_requests:
                params = {"userName": username}
                if cursor:
                    params['cursor'] = cursor

                response = requests.get(url, headers=headers, params=params, timeout=15, verify=False)
                requests_made += 1

                if response.status_code == 200:
                    data = response.json()

                    if data.get('status') == 'success':
                        tweets_data = data.get('data', {})
                        tweets = tweets_data.get('tweets', [])

                        print(f"[INFO] Got {len(tweets)} tweets in this batch (total so far: {len(all_tweets)})")

                        # Extract and clean tweet data
                        for tweet in tweets:
                            tweet_id = tweet.get('id', '')
                            author_username = tweet.get('author', {}).get('userName', username)

                            cleaned_tweet = {
                                'id': tweet_id,
                                'text': tweet.get('text', ''),
                                'created_at': tweet.get('createdAt', ''),
                                'author': tweet.get('author', {}),
                                'metrics': {
                                    'retweet_count': tweet.get('retweetCount', 0),
                                    'reply_count': tweet.get('replyCount', 0),
                                    'like_count': tweet.get('likeCount', 0),
                                    'view_count': tweet.get('viewCount', 0),
                                    'bookmark_count': tweet.get('bookmarkCount', 0),
                                    'quote_count': tweet.get('quoteCount', 0)
                                },
                                'extracted_links': self._extract_links(tweet),
                                'tweet_url': f"https://twitter.com/{author_username}/status/{tweet_id}" if tweet_id else None,
                                'is_thread': tweet.get('replyCount', 0) > 0  # Likely has replies (thread)
                            }
                            all_tweets.append(cleaned_tweet)

                        # Check for next cursor (pagination) - cursor is at root level, not in data
                        has_next_page = data.get('has_next_page', False)
                        cursor = data.get('next_cursor') if has_next_page else None

                        if not cursor or not tweets:
                            break

                    else:
                        error_msg = data.get('msg', 'Unknown API error')
                        return {
                            "success": False,
                            "error": error_msg,
                            "username": username
                        }

                elif response.status_code == 429:
                    return {
                        "success": False,
                        "error": "Rate limit exceeded. Please try again later.",
                        "username": username
                    }

                else:
                    return {
                        "success": False,
                        "error": f"API error: {response.status_code}",
                        "details": response.text,
                        "username": username
                    }

            # Limit to requested amount
            all_tweets = all_tweets[:max_results]

            return {
                "success": True,
                "username": username,
                "user_info": user_info,
                "total_tweets": len(all_tweets),
                "tweets": all_tweets
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Exception: {str(e)}",
                "username": username
            }

    def _extract_links(self, tweet: Dict) -> List[str]:
        """Extract URLs from tweet"""
        links = []

        # Check for URLs in tweet entities
        entities = tweet.get('entities', {})

        # Extract from urls array
        if 'urls' in entities:
            for url_obj in entities['urls']:
                expanded_url = url_obj.get('expandedURL', '') or url_obj.get('expanded_url', '')
                # Skip Twitter/X internal links
                if expanded_url and not any(x in expanded_url.lower() for x in ['twitter.com', 'x.com', 't.co']):
                    links.append(expanded_url)

        # Also check media if present
        if 'media' in entities:
            for media_obj in entities['media']:
                expanded_url = media_obj.get('expandedURL', '') or media_obj.get('expanded_url', '')
                if expanded_url and not any(x in expanded_url.lower() for x in ['twitter.com', 'x.com', 't.co', 'pic.twitter.com']):
                    links.append(expanded_url)

        return links


# Test function
if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    client = TwitterAPIClient()
    result = client.get_user_tweets("elonmusk", max_results=5)

    print(f"Success: {result['success']}")
    print(f"Username: {result.get('username', 'N/A')}")
    print(f"Total tweets: {result.get('total_tweets', 0)}")

    if result['success']:
        print(f"\nUser: {result['user_info'].get('name', 'N/A')}")
        print(f"Followers: {result['user_info'].get('followersCount', 0):,}")

        for i, tweet in enumerate(result['tweets'][:3], 1):
            print(f"\n{i}. {tweet['text'][:100]}...")
            print(f"   Likes: {tweet['metrics']['like_count']}, Retweets: {tweet['metrics']['retweet_count']}")
            print(f"   Links: {tweet.get('extracted_links', [])}")
