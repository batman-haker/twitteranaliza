'use client';

import { useState } from 'react';

interface Tweet {
  id: string;
  text: string;
  created_at: string;
  metrics: {
    like_count: number;
    retweet_count: number;
    reply_count: number;
    view_count: number;
  };
  extracted_links: string[];
  tweet_url?: string;
  is_thread?: boolean;
  analyzed_links?: Array<{
    url: string;
    title?: string;
    summary?: string;
    ai_summary?: string;
    status: string;
  }>;
}

interface AnalyzeResponse {
  success: boolean;
  username: string;
  user_info?: {
    name: string;
    followers: number;
    following: number;
  };
  total_tweets: number;
  tweets: Tweet[];
  error?: string;
  json_file_path?: string;
}

export default function Home() {
  const [username, setUsername] = useState('');
  const [maxTweets, setMaxTweets] = useState(50);
  const [analyzeLinks, setAnalyzeLinks] = useState(true);
  const [saveToJson, setSaveToJson] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username.replace('@', ''),
          max_tweets: maxTweets,
          analyze_links: analyzeLinks,
          save_to_json: saveToJson,
        }),
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({
        success: false,
        username: username,
        total_tweets: 0,
        tweets: [],
        error: 'Błąd połączenia z API',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-center text-gray-800">
          🐦 Twitter/X Analyzer
        </h1>

        {/* Form */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Username (Twitter/X)
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="np. elonmusk"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Liczba tweetów: {maxTweets}
              </label>
              <input
                type="range"
                min="5"
                max="100"
                value={maxTweets}
                onChange={(e) => setMaxTweets(Number(e.target.value))}
                className="w-full"
              />
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="analyzeLinks"
                checked={analyzeLinks}
                onChange={(e) => setAnalyzeLinks(e.target.checked)}
                className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              />
              <label
                htmlFor="analyzeLinks"
                className="ml-2 block text-sm text-gray-900"
              >
                Analizuj linki w postach (Claude AI)
              </label>
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="saveToJson"
                checked={saveToJson}
                onChange={(e) => setSaveToJson(e.target.checked)}
                className="w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500"
              />
              <label
                htmlFor="saveToJson"
                className="ml-2 block text-sm text-gray-900"
              >
                Zapisz wyniki do JSON (z linkami do wątków)
              </label>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-lg disabled:bg-gray-400 disabled:cursor-not-allowed transition"
            >
              {loading ? 'Analizuję...' : 'Analizuj profil'}
            </button>
          </form>
        </div>

        {/* Results */}
        {result && (
          <div className="bg-white rounded-lg shadow-md p-6">
            {result.success ? (
              <>
                {/* User Info */}
                {result.user_info && (
                  <div className="mb-6 pb-6 border-b">
                    <h2 className="text-2xl font-bold mb-2">
                      {result.user_info.name} (@{result.username})
                    </h2>
                    <div className="flex gap-4 text-gray-600">
                      <span>👥 {result.user_info.followers?.toLocaleString()} obserwujących</span>
                      <span>🔗 {result.user_info.following?.toLocaleString()} obserwuje</span>
                    </div>
                  </div>
                )}

                {/* Stats */}
                <div className="mb-6">
                  <p className="text-lg text-gray-700">
                    Znaleziono <strong>{result.total_tweets}</strong> tweetów
                  </p>
                  {result.json_file_path && (
                    <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded-lg">
                      <p className="text-sm text-green-800">
                        ✅ Wyniki zapisane do JSON: <code className="text-xs bg-green-100 px-2 py-1 rounded">{result.json_file_path}</code>
                      </p>
                    </div>
                  )}
                </div>

                {/* Tweets */}
                <div className="space-y-4">
                  {result.tweets.map((tweet, index) => (
                    <div
                      key={index}
                      className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition"
                    >
                      {/* Thread indicator */}
                      {tweet.is_thread && tweet.metrics.reply_count > 0 && (
                        <div className="mb-2 inline-block bg-purple-100 text-purple-800 text-xs px-2 py-1 rounded">
                          🧵 Wątek ({tweet.metrics.reply_count} odpowiedzi)
                        </div>
                      )}

                      <p className="text-gray-800 mb-3">{tweet.text}</p>

                      {/* Tweet URL */}
                      {tweet.tweet_url && (
                        <a
                          href={tweet.tweet_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:underline text-sm mb-3 inline-block"
                        >
                          🔗 Zobacz na Twitter/X →
                        </a>
                      )}

                      {/* Metrics */}
                      <div className="flex gap-4 text-sm text-gray-600 mb-3">
                        <span>❤️ {tweet.metrics.like_count.toLocaleString()}</span>
                        <span>🔁 {tweet.metrics.retweet_count.toLocaleString()}</span>
                        <span>💬 {tweet.metrics.reply_count.toLocaleString()}</span>
                        {tweet.metrics.view_count > 0 && (
                          <span>👀 {tweet.metrics.view_count.toLocaleString()}</span>
                        )}
                      </div>

                      {/* Links */}
                      {tweet.extracted_links && tweet.extracted_links.length > 0 && (
                        <div className="bg-blue-50 rounded p-3">
                          <p className="text-sm font-medium text-blue-900 mb-2">
                            🔗 Linki w poście:
                          </p>
                          {tweet.extracted_links.map((link, linkIndex) => (
                            <div key={linkIndex} className="mb-2">
                              <a
                                href={link}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-blue-600 hover:underline text-sm break-all"
                              >
                                {link}
                              </a>
                            </div>
                          ))}
                        </div>
                      )}

                      {/* Analyzed Links */}
                      {tweet.analyzed_links && tweet.analyzed_links.length > 0 && (
                        <div className="mt-3 space-y-2">
                          {tweet.analyzed_links.map((analyzed, aIndex) => (
                            <div
                              key={aIndex}
                              className="bg-green-50 border border-green-200 rounded p-3"
                            >
                              {analyzed.title && (
                                <h4 className="font-medium text-green-900 mb-1">
                                  {analyzed.title}
                                </h4>
                              )}
                              {analyzed.ai_summary && (
                                <p className="text-sm text-gray-700 italic">
                                  🤖 {analyzed.ai_summary}
                                </p>
                              )}
                              {analyzed.summary && !analyzed.ai_summary && (
                                <p className="text-sm text-gray-600">{analyzed.summary}</p>
                              )}
                            </div>
                          ))}
                        </div>
                      )}

                      <p className="text-xs text-gray-500 mt-2">
                        {new Date(tweet.created_at).toLocaleString('pl-PL')}
                      </p>
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <div className="text-center text-red-600">
                <p className="text-lg font-medium">❌ Błąd</p>
                <p>{result.error}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}
