# ############################################################################################################################################### #
# Question 14:                                                                                                                                    #
# Donner les tweets qui initient une discussion (i.e. une discussion est un enchaîment de tweets deux à deux reliés par un lieu de type REPLY_TO) #
# ############################################################################################################################################### #
from services.tweet.mongodb_tweet_service import get_tweet_text_by_id
from db.mongodb import MongoDB
from db.neo4jdb import Neo4J

# MongoDB tweets
db = MongoDB()
tweets = db.get('tweets', {"replyIdTweet": {"$ne": None}}, {"text": 1, "replyIdTweet": 1})
print("[MongoDB] Tweets qui initient des discussions :")

# Parcours des tweets récupérés et affichage du texte et de la réponse associée.
for i, tweet in enumerate(tweets):
    reply_text = get_tweet_text_by_id(db, tweet['replyIdTweet']) or '[Texte non disponible]'
    print(f"[{i}] \"{tweet['text']}\" -> \"{reply_text}\"")

db.close()

# Neo4J tweets
neo = Neo4J()
query = """
    MATCH (t1:Tweet)-[:REPLY_TO*]->(t2:Tweet)
    WHERE NOT (t2)-[:REPLY_TO]->()
    RETURN t1.text AS text1, t2.text AS text2
"""
tweets = neo.query(query)
print("[Neo4J] Tweets qui initient des discussions :")

# Affichage des textes des tweets et des réponses.
for i, tweet in enumerate(tweets):
    print(f"[{i}] \"{tweet['text1']}\" -> \"{tweet['text2']}\"")

neo.close()
