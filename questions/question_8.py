# ############################################################################ #
# Question 8:                                                                  #
# Donner le nom des utilisateurs suivis par Spinomade (dans ce jeu de données) #
# ############################################################################ #
from services.user.mongodb_user_service import get_following_screennames_by_user_id
from db.mongodb import MongoDB
from db.neo4jdb import Neo4J

user_to_find = "Spinomade"

# MongoDB
db = MongoDB()
# Recherche de l'utilisateur par son nom d'écran dans la collection 'users'
searched_user_doc = db.get_collection('users').find_one({"screenName": user_to_find})

if searched_user_doc:
    searched_user_id = searched_user_doc["idUser"]
    # Utilisation de la fonction de service pour obtenir les noms d'écran des utilisateurs suivis
    result = get_following_screennames_by_user_id(db=db, user_id=searched_user_id)
    following_count = len(result)
    print(f"[MongoDB] Utilisateurs suivis par {user_to_find} ({following_count}): {result}")
else:
    print("[MongoDB] Utilisateur non trouvé.")

db.close()

# Neo4J
neo = Neo4J()
# Requête Cypher pour obtenir les noms des utilisateurs que Spinomade suit
query = "MATCH (u:User {name: $username})-[:FOLLOWS]->(following:User) RETURN following.name AS name"
results = neo.query(query, params={"username": user_to_find})

if results:
    following_users = [record["name"] for record in results]
    following_count = len(following_users)
    print(f"[Neo4J] Utilisateurs suivis par {user_to_find} ({following_count}): {following_users}")
else:
    print("[Neo4J] Utilisateur non trouvé.")

neo.close()
