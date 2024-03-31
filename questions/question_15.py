# ###################################### #
# Question 15:                           #
# Quelle est la plus longue discussion ? #
# ###################################### #
from services.tweet.mongodb_tweet_service import find_longest_thread
from db.neo4jdb import Neo4J
from db.mongodb import MongoDB

# MongoDB
db = MongoDB()
longest_thread = find_longest_thread(db)
print("[MongoDB] La discussion la plus longue :")

if longest_thread:
    discussion = longest_thread[0]
    depth = discussion['numberOfReplies']
    print(f"Longueur de la discussion : {depth}")

    for i, tweet in enumerate(discussion['thread']):
        # La variable `i` représente la profondeur, c'est l'index dans la liste `thread`.
        text = tweet.get('text', '[Texte non disponible]')
        createdAt = tweet.get('createdAt', '[Date non disponible]')
        # Utilisez `i` pour l'affichage de la profondeur de la réponse.
        position = "Tweet initial" if i == 0 else f"Réponse {i}"
        print(f"[{position}]: {text}")
else:
    print("Aucune discussion trouvée.")

db.close()

# Neo4J
neo = Neo4J()
query = """
    MATCH p=(t:Tweet)-[:REPLY_TO*]->(reply:Tweet)
    WITH p, length(p) AS depth
    ORDER BY depth DESC
    LIMIT 1
    UNWIND nodes(p) AS tweet
    RETURN tweet.text AS text, depth
"""
results = neo.query(query)
print("[Neo4J] La discussion la plus longue :")
depth = None

for i, record in enumerate(results):
    if depth is None:
        depth = record['depth']
        print(f"Longueur de la discussion : {depth}")
    position = "Tweet initial" if i == 0 else f"Réponse {i}"
    print(f"[{position}]: {record['text']}")

neo.close()
