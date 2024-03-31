# ########################## #
# Question 2:                #
# Donner le nombre de tweets #
# ########################## #
from db.mongodb import MongoDB
from db.neo4jdb import Neo4J

# MongoDB
db = MongoDB()
tweet_count = db.count('tweets')
print(f"[MongoDB] Nombre de tweets: {tweet_count}")
db.close()

# Neo4J
neo = Neo4J()
tweet_count = neo.query("MATCH (n:Tweet) RETURN COUNT(n) AS count")
print(f"[Neo4J] Nombre de tweets: {tweet_count[0]['count']}")
neo.close()
