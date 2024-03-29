# ############################################################################################################### #
# Question 12:                                                                                                    #
# Donner les 10 tweets les plus populaires (i.e la popularité se mesure au nombre de fois où le tweet est favori) #
# ############################################################################################################### #
from services.tweet.mongodb_tweet_service import get_most_popular_tweets
from db.mongdb import MongoDB

db = MongoDB()
tweets = get_most_popular_tweets(db, 10)
print(f"10 most popular tweets:")

for tweet in tweets:
    print(f"{tweet['_id']} ({tweet['nbFavorites']} ❤️): {tweet['text']}")
db.close()
