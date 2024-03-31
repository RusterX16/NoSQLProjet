# ######################################################## #
# Question 6:                                              #
# Donner les tweets qui sont des réponses à un autre tweet #
# ######################################################## #
from db.mongodb import MongoDB
from db.neo4jdb import Neo4J

# MongoDB
db = MongoDB()
# On cherche les tweets qui ont un champ 'replyIdTweet' non nul, indiquant qu'ils sont des réponses
initial_match = {"replyIdTweet": {"$ne": None}}
results = db.get('tweets', initial_match)

if results:
    for i, result in enumerate(results):
        print(f"[MongoDB] [{i+1}] {result['idTweet']}: {result['text']}")
else:
    print("[MongoDB] Aucun tweet de réponse trouvé.")

db.close()

# Neo4J
neo = Neo4J()
# Requête Cypher pour trouver les tweets répondant à d'autres tweets
# Cette requête retourne les tweets qui sont la cible d'une relation 'REPLY_TO'
query = """
MATCH (original:Tweet)-[:REPLY_TO]->(reply:Tweet)
RETURN reply.id AS idTweet, reply.text AS text
"""
results = neo.query(query)

if results:
    for i, record in enumerate(results):
        print(f"[Neo4J] [{i + 1}] {record['idTweet']}: {record['text']}")
else:
    print("[Neo4J] Aucun tweet de réponse trouvé.")

neo.close()
