# ########################### #
# Question 3:                 #
# Donner le nombre d'hashtags #
# ########################### #
from db.mongodb import MongoDB
from db.neo4jdb import Neo4J

# MongoDB
db = MongoDB()
hashtag_count = db.count('hashtags')
print(f"[MongoDB] Nombre d'hashtags: {hashtag_count}")
db.close()

# Neo4J
neo = Neo4J()
hashtag_count = neo.query("MATCH (n:Hashtag) RETURN COUNT(n) AS count")
print(f"[Neo4J] Nombre d'hashtags: {hashtag_count[0]['count']}")
neo.close()
