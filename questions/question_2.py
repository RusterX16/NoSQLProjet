# ########################## #
# Question 2:                #
# Donner le nombre de tweets #
# ########################## #
from db.mongdb import MongoDB
from db.neo4jdb import Neo4J

db = MongoDB()
tweet_count = db.count('tweets')
print(f"[MongoDB] Nombre de tweets: {tweet_count}")
db.close()

neo = Neo4J()
tweet_count = neo.query("MATCH (n:Tweet) RETURN COUNT(n) AS count")
print(f"[Neo4J] Nombre de tweets: {tweet_count}")
neo.close()
