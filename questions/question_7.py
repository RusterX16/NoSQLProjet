# ################################################################# #
# Question 7:                                                       #
# Donner le nom des followers de Spinomade (dans ce jeu de données) #
# ################################################################# #
from services.user.mongodb_user_service import get_follower_screennames_by_user_id
from db.mongdb import MongoDB
from db.neo4jdb import Neo4J

user_to_find = "Spinomade"

db = MongoDB()
searched_user_doc = db.get_collection('users').find_one({"screenName": f"{user_to_find}"})

if searched_user_doc:
    searched_user_id = searched_user_doc["idUser"]
    result = get_follower_screennames_by_user_id(db=db, user_id=searched_user_id)
    follower_count = len(result)
    print(f"[MongoDB] Followers de {user_to_find} ({follower_count}): {result}")
else:
    print("[MongoDB] User not found.")

db.close()

neo = Neo4J()
query = "MATCH (u:User)<-[:FOLLOWS]-(f:User) WHERE u.name = $username RETURN f.name AS name"
results = neo.query(query, params={"username": user_to_find})

if results:
    follower_count = len(results)
    followers = [record["name"] for record in results]
    print(f"[Neo4J] Followers de {user_to_find} ({follower_count}): {followers}")
else:
    print("[Neo4J] User not found.")

neo.close()
