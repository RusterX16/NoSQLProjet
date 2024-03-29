# ########################### #
# Question 3:                 #
# Donner le nombre d'hashtags #
# ########################### #
from db.mongdb import MongoDB
from db.neo4jdb import Neo4J

db = MongoDB()
hashtag_count = (db.count('hashtags'))
print(f"[MongoDB] Nombre d'hashtags: {hashtag_count}")
db.close()

neo = Neo4J()
hashtag_count = neo.query("MATCH (n:Hashtag) RETURN COUNT(n) AS count")
print(f"[Neo4J] Nombre d'hashtags: {hashtag_count}")
neo.close()
