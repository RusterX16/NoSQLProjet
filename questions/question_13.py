# #################################################################################################################### #
# Question 13:                                                                                                         #
# Donner les 10 hashtags les plus populaires (i.e la popularité se mesure au nombre de fois où le hashtag est utilisé) #
# #################################################################################################################### #
from services.hashtag.mongodb_hashtag_service import get_most_popular_hashtags
from db.mongdb import MongoDB

db = MongoDB()
hashtags = get_most_popular_hashtags(db, 10)
print("Top 10 Most Popular Hashtags:")
for hashtag in hashtags:
    print(f"#{hashtag['_id']} ({hashtag['unique_tweet_count']})")
db.close()
