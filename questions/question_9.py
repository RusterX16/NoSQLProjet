# ##################################################################################### #
# Question 9:                                                                           #
# Donner le nom des utilisateurs qui sont à la fois followers et followees de Spinomade #
# ##################################################################################### #
from services.user.mongodb_user_service import get_mutual_screennames_by_user_id
from services.user.neo4j_user_service import get_mutual_by_user
from db.mongodb import MongoDB
from db.neo4jdb import Neo4J

user_to_find = "Spinomade"

# MongoDB
db = MongoDB()
user_doc = db.get_collection('users').find_one({"screenName": user_to_find})
if user_doc:
    user_id = user_doc["idUser"]
    mutual_users = get_mutual_screennames_by_user_id(db=db, user_id=user_id)
    print(f"[MongoDB] Utilisateurs mutuels de {user_to_find} ({len(mutual_users)}): {mutual_users}")
db.close()

# Neo4J
neo = Neo4J()
mutual_users = get_mutual_by_user(db=neo, name=user_to_find)
print(f"[Neo4J] Utilisateurs mutuels de {user_to_find} ({len(mutual_users)}): {mutual_users}")
neo.close()
