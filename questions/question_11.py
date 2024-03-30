# ################################################################################## #
# Question 11:                                                                       #
# Donner les utilisateurs qui follow plus de 5 utilisateurs (dans ce jeu de données) #
# ################################################################################## #
from db.neo4jdb import Neo4J
from services.user.mongodb_user_service import get_users_screennames_with_more_than_n_followings
from db.mongdb import MongoDB
from services.user.neo4j_user_service import get_users_names_with_more_than_n_followings

db = MongoDB()
users = get_users_screennames_with_more_than_n_followings(db, 5)
print(f"Users following more than 5 users ({len(users)}): {users}")
db.close()

neo = Neo4J()
users = get_users_names_with_more_than_n_followings(neo, 5)
print(f"Users following more than 5 users ({len(users)}): {users}")
neo.close()
