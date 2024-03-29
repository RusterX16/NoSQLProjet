# ############################################################################ #
# Question 8:                                                                  #
# Donner le nom des utilisateurs suivis par Spinomade (dans ce jeu de données) #
# ############################################################################ #
from db.neo4jdb import Neo4J
from services.user.mongodb_user_service import get_following_screennames_by_user_id
from db.mongdb import MongoDB

user_to_find = "Spinomade"

db = MongoDB()
searched_user_doc = db.get_collection('users').find_one({"screenName": user_to_find})

if searched_user_doc:
    searched_user_id = searched_user_doc["idUser"]
    result = get_following_screennames_by_user_id(db=db, user_id=searched_user_id)
    following_count = len(result)
    print(f"Utilisateurs suivis par {user_to_find} ({following_count}): {result}")
else:
    print("User not found.")

db.close()

neo = Neo4J()
query = f"MATCH (u:User {name: '{user_to_find}'})-[:FOLLOWS]->(following:User) RETURN following.name AS name"
results = neo.query(query, params={"username": user_to_find})

if results:
    following_users = [record["name"] for record in results]
    following_count = len(following_users)
    print(f"Utilisateurs suivis par {user_to_find} ({following_count}): {following_users}")
else:
    print(f"No users are followed by {user_to_find}.")

neo.close()