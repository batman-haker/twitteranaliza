"""
Link Analyzer - Analyzes article links from tweets
Uses Claude API to summarize content
"""
import requests
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv
from anthropic import Anthropic
from bs4 import BeautifulSoup
from pathlib import Path

# Load .env from parent directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class LinkAnalyzer:
    """Analyzes links from tweets"""

    def __init__(self):
        self.claude_api_key = os.getenv('CLAUDE_API_KEY')
        if self.claude_api_key:
            self.claude = Anthropic(api_key=self.claude_api_key)
        else:
            self.claude = None
            print("Warning: CLAUDE_API_KEY not found. Link analysis will be limited.")

    def analyze_links(self, tweets: List[Dict]) -> List[Dict]:
        """
        Analyze all links in tweets

        Args:
            tweets: List of tweet dictionaries

        Returns:
            List of tweets with analyzed links
        """
        analyzed_tweets = []

        for tweet in tweets:
            tweet_copy = tweet.copy()
            links = tweet.get('extracted_links', [])

            if links:
                tweet_copy['analyzed_links'] = []

                for link in links:
                    analysis = self._analyze_single_link(link)
                    tweet_copy['analyzed_links'].append(analysis)

            analyzed_tweets.append(tweet_copy)

        return analyzed_tweets

    def _analyze_single_link(self, url: str) -> Dict:
        """
        Analyze a single link

        Returns:
            Dict with url, title, summary, and analysis status
        """
        result = {
            "url": url,
            "title": None,
            "summary": None,
            "status": "pending"
        }

        try:
            # Fetch the page
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10, verify=False)

            if response.status_code != 200:
                result['status'] = 'error'
                result['error'] = f"HTTP {response.status_code}"
                return result

            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')

            # Get title
            title_tag = soup.find('title')
            if title_tag:
                result['title'] = title_tag.get_text().strip()

            # Get meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                result['summary'] = meta_desc.get('content').strip()

            # If Claude is available, get AI summary
            if self.claude and response.text:
                try:
                    # Get main text content
                    paragraphs = soup.find_all('p')
                    content_text = ' '.join([p.get_text() for p in paragraphs[:10]])  # First 10 paragraphs

                    if len(content_text) > 200:
                        ai_summary = self._get_claude_summary(content_text[:2000], url)
                        if ai_summary:
                            result['ai_summary'] = ai_summary
                except Exception as e:
                    print(f"Claude analysis failed for {url}: {e}")

            result['status'] = 'success'

        except requests.Timeout:
            result['status'] = 'error'
            result['error'] = 'Timeout'
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)

        return result

    def _get_claude_summary(self, content: str, url: str) -> Optional[str]:
        """Get AI summary from Claude"""
        if not self.claude:
            return None

        try:
            prompt = f"""Przeanalizuj poniższą treść artykułu i napisz krótkie podsumowanie (2-3 zdania) po polsku.

URL: {url}

Treść:
{content}

Odpowiedz tylko podsumowaniem, bez dodatkowych komentarzy."""

            message = self.claude.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=300,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            return message.content[0].text

        except Exception as e:
            print(f"Claude API error: {e}")
            return None


# Test function
if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    analyzer = LinkAnalyzer()

    # Test link
    test_link = "https://techcrunch.com/2024/01/15/openai-gpt-4-turbo/"

    print("Analyzing link...")
    result = analyzer._analyze_single_link(test_link)

    print(f"\nURL: {result['url']}")
    print(f"Status: {result['status']}")
    print(f"Title: {result.get('title', 'N/A')}")
    print(f"Summary: {result.get('summary', 'N/A')}")
    print(f"AI Summary: {result.get('ai_summary', 'N/A')}")
