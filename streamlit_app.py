"""
Twitter Analyzer - Streamlit Web App
Simple interface for fetching and analyzing Twitter/X profiles
"""

import streamlit as st
import sys
import os
from pathlib import Path
import json
from datetime import datetime

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from twitter_client import TwitterAPIClient

# Page config
st.set_page_config(
    page_title="Twitter Analyzer",
    page_icon="🐦",
    layout="wide"
)

# Title
st.title("🐦 Twitter/X Analyzer")
st.markdown("Fetch and analyze tweets from any Twitter/X profile")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    username = st.text_input(
        "Username (without @)",
        placeholder="elonmusk",
        help="Enter Twitter/X username without @"
    )

    max_tweets = st.slider(
        "Number of tweets",
        min_value=5,
        max_value=100,
        value=50,
        step=5,
        help="How many tweets to fetch"
    )

    save_json = st.checkbox(
        "Save to JSON",
        value=False,
        help="Save results to exports/ folder"
    )

    analyze_button = st.button("🔍 Analyze Profile", type="primary", use_container_width=True)

# Initialize session state
if 'result' not in st.session_state:
    st.session_state.result = None

# Main content
if analyze_button and username:
    with st.spinner(f"Fetching {max_tweets} tweets from @{username}..."):
        try:
            # Initialize client
            client = TwitterAPIClient()

            # Fetch tweets
            result = client.get_user_tweets(username=username, max_results=max_tweets)

            if result['success']:
                st.session_state.result = result

                # Save to JSON if requested
                if save_json:
                    exports_dir = Path(__file__).parent / 'exports'
                    exports_dir.mkdir(exist_ok=True)

                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{username}_{timestamp}.json"
                    filepath = exports_dir / filename

                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(result, f, ensure_ascii=False, indent=2)

                    st.success(f"✅ Saved to: {filepath}")
            else:
                st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                st.session_state.result = None

        except Exception as e:
            st.error(f"❌ Exception: {str(e)}")
            st.session_state.result = None

# Display results
if st.session_state.result:
    result = st.session_state.result

    # User info
    if result.get('user_info'):
        user_info = result['user_info']

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Account",
                f"@{result['username']}",
                user_info.get('name', 'N/A')
            )

        with col2:
            followers = user_info.get('followersCount', 0)
            st.metric("Followers", f"{followers:,}" if isinstance(followers, int) else followers)

        with col3:
            following = user_info.get('followingCount', 0)
            st.metric("Following", f"{following:,}" if isinstance(following, int) else following)

        st.divider()

    # Tweets
    st.subheader(f"📝 {result['total_tweets']} Tweets")

    for i, tweet in enumerate(result['tweets'], 1):
        with st.expander(f"Tweet {i} - {tweet.get('created_at', 'N/A')}", expanded=(i <= 3)):
            # Tweet text
            st.markdown(f"**{tweet['text']}**")

            # Metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                likes = tweet['metrics'].get('like_count', 0)
                st.metric("❤️ Likes", f"{likes:,}" if isinstance(likes, int) else likes)

            with col2:
                retweets = tweet['metrics'].get('retweet_count', 0)
                st.metric("🔁 Retweets", f"{retweets:,}" if isinstance(retweets, int) else retweets)

            with col3:
                replies = tweet['metrics'].get('reply_count', 0)
                st.metric("💬 Replies", f"{replies:,}" if isinstance(replies, int) else replies)

            with col4:
                views = tweet['metrics'].get('view_count', 0)
                if views > 0:
                    st.metric("👀 Views", f"{views:,}" if isinstance(views, int) else views)

            # Thread indicator
            if tweet.get('is_thread'):
                st.info("🧵 This tweet is part of a thread")

            # Links
            if tweet.get('extracted_links'):
                st.markdown("**🔗 External Links:**")
                for link in tweet['extracted_links']:
                    st.markdown(f"- {link}")

            # Tweet URL
            if tweet.get('tweet_url'):
                st.markdown(f"[View on Twitter/X →]({tweet['tweet_url']})")

elif not st.session_state.result:
    # Welcome message
    st.info("""
    👋 **Welcome to Twitter Analyzer!**

    Enter a Twitter/X username in the sidebar and click "Analyze Profile" to get started.

    **Features:**
    - ✅ Fetch 5-100 tweets from any public profile
    - ✅ View tweet metrics (likes, retweets, views)
    - ✅ Extract external links
    - ✅ Identify threads
    - ✅ Save results to JSON

    **Example usernames:** elonmusk, naval, stocktavia, realDonaldTrump
    """)

    # Example
    with st.expander("📖 How to use"):
        st.markdown("""
        1. **Enter username** (without @) in the sidebar
        2. **Choose number of tweets** (5-100 with slider)
        3. **Optional:** Check "Save to JSON" to export results
        4. Click **"Analyze Profile"** button
        5. View results below!

        **Note:** This uses TwitterAPI.io which has rate limits.
        If you hit limits, wait a few minutes and try again.
        """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.8em;'>
    Made with ❤️ using Streamlit | Data from TwitterAPI.io
</div>
""", unsafe_allow_html=True)
