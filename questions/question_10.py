# ########################################################################### #
# Question 10:                                                                #
# Donner les utilisateurs ayant plus de 10 followers (dans ce jeu de données) #
# ########################################################################### #
from db.mongodb_user_service import get_users_screennames_with_more_than_n_followers
from db.mongdb import MongoDB

db = MongoDB()
users = get_users_screennames_with_more_than_n_followers(db, 10)
print(f"Users with more than 10 followers ({len(users)}): {users}")
db.close()
