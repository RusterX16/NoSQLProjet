# ######################################################## #
# Question 6:                                              #
# Donner les tweets qui sont des réponses à un autre tweet #
# ######################################################## #
from db.mongdb import MongoDB
from db.neo4jdb import Neo4J

db = MongoDB()
initial_match = {"replyIdTweet": {"$ne": None}}
results = db.get('tweets', initial_match)

if results:
    for i, result in enumerate(results):
        print(f"[MongoDB] [{i+1}] {result['idTweet']}: {result['text']}")
else:
    print("[MongoDB] No reply tweets found.")

db.close()

neo = Neo4J()
query = "MATCH (:Tweet)-[:REPLY_TO]->(reply:Tweet) RETURN reply"
results = neo.query(query)

if results:
    for i, record in enumerate(results):
        tweet = record['reply']
        print(f"[Neo4J] [{i + 1}] {tweet['id']}: {tweet['text']}")
else:
    print("[Neo4J] No reply tweets found.")

neo.close()