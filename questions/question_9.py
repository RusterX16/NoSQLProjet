# ##################################################################################### #
# Question 9:                                                                           #
# Donner le nom des utilisateurs qui sont à la fois followers et followees de Spinomade #
# ##################################################################################### #
from services.user.mongodb_user_service import get_mutual_screennames_by_user_id
from services.user.neo4j_user_service import get_mutual_by_user
from db.neo4jdb import Neo4J
from db.mongdb import MongoDB

user_to_find = "Spinomade"

db = MongoDB()
user_doc = db.get_collection('users').find_one({"screenName": user_to_find})

if user_doc:
    user_id = user_doc["idUser"]
    # Get the mutual screen names using the user ID
    result = get_mutual_screennames_by_user_id(db=db, user_id=user_id)
    mutual_count = len(result)
    print(f"[MongoDB] Utilisateurs mutuels de {user_to_find} ({mutual_count}): {result}")

db.close()


neo = Neo4J()
query = get_mutual_by_user(db=neo, name=user_to_find)

if query:
    mutual_count = len(query)
    print(f"[Neo4J] Utilisateurs mutuels de {user_to_find} ({mutual_count}): {query}")
else:
    print(f"[Neo4J] No mutual users found for {user_to_find}.")

neo.close()
