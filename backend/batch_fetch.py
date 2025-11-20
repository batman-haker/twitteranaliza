"""
Batch Twitter Fetcher
Fetches last 50 tweets from multiple accounts and saves each to separate JSON
"""
import json
from datetime import datetime
from pathlib import Path
import urllib3
from twitter_client import TwitterAPIClient
from link_analyzer import LinkAnalyzer

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Lista kont do pobrania
ACCOUNTS_TO_FETCH = [
    "elonmusk",
    "BillGates",
    "BarackObama",
    # Dodaj tutaj więcej kont
]

def fetch_and_save_account(username: str, max_tweets: int = 50, analyze_links: bool = True):
    """
    Fetch tweets from one account and save to JSON

    Args:
        username: Twitter username (without @)
        max_tweets: Number of tweets to fetch
        analyze_links: Whether to analyze links with Claude AI
    """
    print(f"\n{'='*60}")
    print(f"Fetching tweets for @{username}...")
    print(f"{'='*60}")

    try:
        # Initialize clients
        twitter_client = TwitterAPIClient()
        link_analyzer = LinkAnalyzer() if analyze_links else None

        # Fetch tweets
        result = twitter_client.get_user_tweets(
            username=username,
            max_results=max_tweets
        )

        if not result['success']:
            print(f"ERROR for @{username}: {result.get('error', 'Unknown error')}")
            return False

        tweets = result['tweets']

        # Analyze links if requested
        if analyze_links and tweets and link_analyzer:
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
            "fetched_at": datetime.now().isoformat()
        }

        # Create exports directory if it doesn't exist
        exports_dir = Path(__file__).parent.parent / 'exports' / 'batch'
        exports_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{username}_{timestamp}.json"
        filepath = exports_dir / filename

        # Save to JSON with pretty formatting
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(response_data, f, ensure_ascii=False, indent=2)

        print(f"SUCCESS! Saved {len(tweets)} tweets to: {filepath}")

        # Print user stats
        if result.get('user_info'):
            info = result['user_info']
            print(f"   User: {info.get('name', 'N/A')}")
            print(f"   Followers: {info.get('followersCount', 0):,}")
            print(f"   Following: {info.get('followingCount', 0):,}")

        return True

    except Exception as e:
        print(f"EXCEPTION for @{username}: {str(e)}")
        return False


def batch_fetch_accounts(accounts: list, max_tweets: int = 50, analyze_links: bool = True):
    """
    Fetch tweets from multiple accounts

    Args:
        accounts: List of Twitter usernames
        max_tweets: Number of tweets per account
        analyze_links: Whether to analyze links
    """
    print("\n" + "="*60)
    print("BATCH TWITTER FETCHER")
    print("="*60)
    print(f"Accounts to process: {len(accounts)}")
    print(f"Tweets per account: {max_tweets}")
    print(f"Analyze links: {'Yes' if analyze_links else 'No'}")
    print("="*60)

    results = {
        'success': [],
        'failed': []
    }

    for i, username in enumerate(accounts, 1):
        print(f"\n[{i}/{len(accounts)}] Processing @{username}...")

        success = fetch_and_save_account(
            username=username,
            max_tweets=max_tweets,
            analyze_links=analyze_links
        )

        if success:
            results['success'].append(username)
        else:
            results['failed'].append(username)

    # Summary
    print("\n" + "="*60)
    print("BATCH FETCH SUMMARY")
    print("="*60)
    print(f"Successful: {len(results['success'])} accounts")
    if results['success']:
        for username in results['success']:
            print(f"   - @{username}")

    print(f"\nFailed: {len(results['failed'])} accounts")
    if results['failed']:
        for username in results['failed']:
            print(f"   - @{username}")

    print(f"\nTotal processed: {len(accounts)} accounts")
    print("="*60)

    return results


if __name__ == "__main__":
    # Lista kont do pobrania
    accounts = [
        # Giełda (16 accounts)
        "stocktavia",
        "PelosiTracker_",
        "wallstengine",
        "ksochanek",
        "Dan_Kostecki",
        "HayekAndKeynes",
        "Inwestomat_eu",
        "hedgefundowiec",
        "rditrych",
        "Maciej__Czajka",
        "PiotrZolkiewicz",
        "PawelMalik_GG",
        "AnalitykF",
        "conksresearch",
        "sentimentrader",
        "Joker68069137",

        # Kryptowaluty (5 accounts)
        "KO_Kryptowaluty",
        "Dystopia_PL",
        "Dziewczynka_z_",
        "wesleyplpl",
        "Paul__Crow",

        # Gospodarka (3 accounts)
        "wstepien_",
        "KamSobolewski",
        "T_Smolarek",

        # Polityka (2 accounts)
        "realDonaldTrump",
        "MikolajVonskyT",

        # Nowinki AI (4 accounts)
        "popai_pl",
        "huggingface",
        "rpl_0x",
        "miroburn",

        # Filozofia (3 accounts)
        "orangebook_",
        "naval",
        "andrzejdragan",
    ]

    # Konfiguracja
    MAX_TWEETS = 50  # Liczba tweetów na konto
    ANALYZE_LINKS = False  # Czy analizować linki (True = wolniejsze, ale z analizą AI)

    print(f"Total accounts to fetch: {len(accounts)}")
    print(f"Tweets per account: {MAX_TWEETS}")
    print(f"Files will be saved to: twitter-analyzer/exports/batch/\n")

    # Uruchom batch fetch
    batch_fetch_accounts(
        accounts=accounts,
        max_tweets=MAX_TWEETS,
        analyze_links=ANALYZE_LINKS
    )
