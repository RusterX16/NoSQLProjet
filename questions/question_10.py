# ########################################################################### #
# Question 10:                                                                #
# Donner les utilisateurs ayant plus de 10 followers (dans ce jeu de données) #
# ########################################################################### #
from services.user.mongodb_user_service import get_users_screennames_with_more_than_n_followers
from services.user.neo4j_user_service import get_users_names_with_more_than_n_followers
from db.mongodb import MongoDB
from db.neo4jdb import Neo4J

# MongoDB
mongo_db = MongoDB()
mongo_users = get_users_screennames_with_more_than_n_followers(mongo_db, 10)
print(f"[MongoDB] Utilisateurs avec plus de 10 followers ({len(mongo_users)}): {mongo_users}")
mongo_db.close()

# Neo4J
neo_db = Neo4J()
neo_users = get_users_names_with_more_than_n_followers(neo_db, 10)
print(f"[Neo4J] Utilisateurs avec plus de 10 followers ({len(neo_users)}): {neo_users}")
neo_db.close()
