# #################################################################################################################### #
# Question 13:                                                                                                         #
# Donner les 10 hashtags les plus populaires (i.e la popularité se mesure au nombre de fois où le hashtag est utilisé) #
# #################################################################################################################### #
from services.hashtag.mongodb_hashtag_service import get_most_popular_hashtags as get_most_popular_hashtags_mongo
from services.hashtag.neo4j_hashtag_service import get_most_popular_hashtags as get_most_popular_hashtags_neo
from db.mongdb import MongoDB
from db.neo4jdb import Neo4J

db = MongoDB()
hashtags = get_most_popular_hashtags_mongo(db, 10)
print("[MongoDB] Top 10 Most Popular Hashtags:")

for i, hashtag in enumerate(hashtags):
    print(f"[{i}] #{hashtag['_id']} ({hashtag['unique_tweet_count']})")

db.close()

neo = Neo4J()
hashtags = get_most_popular_hashtags_neo(neo, 10)
print("[Neo4J] Top 10 Most Popular Hashtags:")

for i, hashtag in enumerate(hashtags):
    print(f"[{i}] #{hashtag['hashtag']} ({hashtag['tweetCount']})")

neo.close()
