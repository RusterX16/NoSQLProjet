# ############################################################################################################################################### #
# Question 14:                                                                                                                                    #
# Donner les tweets qui initient une discussion (i.e. une discussion est un enchaîment de tweets deux à deux reliés par un lieu de type REPLY_TO) #
# ############################################################################################################################################### #
from services.tweet.mongodb_tweet_service import get_tweet_text_by_id
from db.mongdb import MongoDB
from db.neo4jdb import Neo4J

# MongoDB tweets
db = MongoDB()
tweets = db.get('tweets', {"replyIdTweet": {"$ne": None}}, {"text": 1, "replyIdTweet": 1})
print("[MongoDB] Tweets initiating discussions:")

for i, tweet in enumerate(tweets):
    print(f"[{i}] {tweet['_id']} {tweet['text']} -> replies to \"{get_tweet_text_by_id(db, id_tweet=tweet['replyIdTweet'])}\"")

db.close()

# Neo4J tweets
neo = Neo4J()
query = """
    MATCH (t1:Tweet)-[:REPLY_TO*]->(t2:Tweet)
    WHERE NOT (t2)-[:REPLY_TO]->()
    RETURN t1.text AS text1, t2.text AS text2
    """
tweets = neo.query(query)
print("[Neo4J] Tweets initiating discussions:")

for i, tweet in enumerate(tweets):
    print(f"[{i}] {tweet['text1']} -> {tweet['text2']}")

neo.close()
