# ################################################################################## #
# Question 11:                                                                       #
# Donner les utilisateurs qui follow plus de 5 utilisateurs (dans ce jeu de données) #
# ################################################################################## #
from db.mongodb import MongoDB
from db.neo4jdb import Neo4J
from services.user.mongodb_user_service import get_users_screennames_with_more_than_n_followings
from services.user.neo4j_user_service import get_users_names_with_more_than_n_followings

# MongoDB
mongo_db = MongoDB()
mongo_users = get_users_screennames_with_more_than_n_followings(mongo_db, 5)
print(f"[MongoDB] Utilisateurs suivant plus de 5 utilisateurs ({len(mongo_users)}): {mongo_users}")
mongo_db.close()

# Neo4J
neo_db = Neo4J()
neo_users = get_users_names_with_more_than_n_followings(neo_db, 5)
print(f"[Neo4J] Utilisateurs suivant plus de 5 utilisateurs ({len(neo_users)}): {neo_users}")
neo_db.close()
