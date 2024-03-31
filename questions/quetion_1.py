# ############################### #
# Question 1:                     #
# Donner le nombre d'utilisateurs #
# ############################### #
from db.mongodb import MongoDB
from db.neo4jdb import Neo4J

# MongoDB.
db = MongoDB()
user_count = db.count('users')
print(f"[MongoDB] Nombre d'utilisateur: {user_count}")
db.close()  # Assure la fermeture de la connexion à la base de données.

# Neo4J.
neo = Neo4J()
user_count = neo.query("MATCH (n:User) RETURN COUNT(n) AS count")
print(f"[Neo4J] Nombre d'utilisateur: {user_count[0]['count']}")
neo.close()
