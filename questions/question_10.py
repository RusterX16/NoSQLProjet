# ########################################################################### #
# Question 10:                                                                #
# Donner les utilisateurs ayant plus de 10 followers (dans ce jeu de données) #
# ########################################################################### #
from services.user.mongodb_user_service import get_users_screennames_with_more_than_n_followers
from services.user.neo4j_user_service import get_users_names_with_more_than_n_followers
from db.mongdb import MongoDB
from db.neo4jdb import Neo4J

db = MongoDB()
users = get_users_screennames_with_more_than_n_followers(db, 10)
print(f"[MongoDB] Users with more than 10 followers ({len(users)}): {users}")
db.close()

neo = Neo4J()
users = get_users_names_with_more_than_n_followers(neo, 10)
print(f"[Neo4J] Users with more than 10 followers ({len(users)}): {users}")
neo.close()
