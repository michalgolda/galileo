import os
from dotenv import load_dotenv
from aggregators import TokenInsightAggregator
from dataclasses import dataclass

load_dotenv()

TOKENINISIGHT_API_KEY = os.environ.get("TOKENINSIGHT_API_KEY", None)
if not TOKENINISIGHT_API_KEY:
    raise ValueError("TOKENINSIGHT_API_KEY environment variable is required.")

TOKENINISIGHT_API_URL = os.environ.get("TOKENINSIGHT_API_URL")
if not TOKENINISIGHT_API_URL:
    raise ValueError("TOKENINSIGHT_API_URL environment variable is required.")


tokeninsight_aggregator = TokenInsightAggregator(TOKENINISIGHT_API_URL, TOKENINISIGHT_API_KEY)

top_ten_coins = tokeninsight_aggregator.getTopCoins()
print("Top ten coins: ", top_ten_coins, "\n\n")

rating_score_sum = 0

for coin in top_ten_coins:
    rating = tokeninsight_aggregator.getRating(coin)
    rating_score_sum += rating.rating_score
    
    print(coin, rating, "\n\n")

print("Average top ten coins rating: ", rating_score_sum / 10)
