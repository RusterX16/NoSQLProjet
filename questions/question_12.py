# ################################################################################################################## #
# Question 12:                                                                                                       #
# Donner les 10 tweets les plus populaires (i.e. la popularite se mesure au nombre de fois où le# tweet est favori.) #
# ################################################################################################################## #
from db.mongodb import MongoDB
from db.neo4jdb import Neo4J
from services.tweet.mongodb_tweet_service import get_most_popular_tweets as get_most_popular_tweets_mongo
from services.tweet.neo4j_tweet_service import get_most_popular_tweets as get_most_popular_tweets_neo

# MongoDB
mongo_db = MongoDB()
mongo_tweets = get_most_popular_tweets_mongo(mongo_db, 10)
print("[MongoDB] 10 tweets les plus populaires :")
for i, tweet in enumerate(mongo_tweets):
    print(f"[{i}] {tweet['_id']} ({tweet['nbFavorites']} ❤️): {tweet['text']}")
mongo_db.close()

# Neo4J
neo_db = Neo4J()
neo_tweets = get_most_popular_tweets_neo(neo_db, 10)
print("[Neo4J] 10 tweets les plus populaires :")
for i, tweet in enumerate(neo_tweets):
    print(f"[{i}] {tweet['idTweet']} ({tweet['nbFavorites']} ❤️): {tweet['text']}")
neo_db.close()
