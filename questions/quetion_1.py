# ############################### #
# Question 1:                     #
# Donner le nombre d'utilisateurs #
# ############################### #
from db.mongdb import MongoDB
from db.neo4jdb import Neo4J

db = MongoDB()
user_count = db.count('users')
print(f"[MongoDB] Nombre d'utilisateur: {user_count}")
db.close()

neo = Neo4J()
user_count = neo.query("MATCH (n:User) RETURN COUNT(n) AS count")
print(f"[Neo4J] Nombre d'utilisateur: {user_count}")
neo.close()
