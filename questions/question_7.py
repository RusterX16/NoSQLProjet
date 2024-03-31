# ################################################################# #
# Question 7:                                                       #
# Donner le nom des followers de Spinomade (dans ce jeu de données) #
# ################################################################# #
from db.mongodb import MongoDB
from db.neo4jdb import Neo4J
from services.user.mongodb_user_service import get_follower_screennames_by_user_id

# Nom de l'utilisateur ciblé
user_to_find = "Spinomade"

# MongoDB
db = MongoDB()
# Recherche du document de l'utilisateur dans la collection 'users'
searched_user_doc = db.get_collection('users').find_one({"screenName": user_to_find})

if searched_user_doc:
    searched_user_id = searched_user_doc["idUser"]
    # Utilisation d'une fonction de service pour obtenir les noms d'écran des followers
    result = get_follower_screennames_by_user_id(db=db, user_id=searched_user_id)
    follower_count = len(result)
    print(f"[MongoDB] Followers de {user_to_find} ({follower_count}): {result}")
else:
    print("[MongoDB] Utilisateur non trouvé.")

db.close()

# Neo4J
neo = Neo4J()
# Requête Cypher pour obtenir les noms des followers de l'utilisateur
query = "MATCH (u:User)<-[:FOLLOWS]-(f:User) WHERE u.name = $username RETURN f.name AS name"
results = neo.query(query, params={"username": user_to_find})

if results:
    followers = [record["name"] for record in results]
    follower_count = len(followers)
    print(f"[Neo4J] Followers de {user_to_find} ({follower_count}): {followers}")
else:
    print("[Neo4J] Utilisateur non trouvé.")

neo.close()
