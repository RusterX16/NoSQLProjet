# ################################################################################## #
# Question 11:                                                                       #
# Donner les utilisateurs qui follow plus de 5 utilisateurs (dans ce jeu de données) #
# ################################################################################## #
from db.mongodb_user_service import get_users_screennames_with_more_than_n_followees
from db.mongdb import MongoDB

db = MongoDB()
users = get_users_screennames_with_more_than_n_followees(db, 5)
print(f"Users following more than 5 users ({len(users)}): {users}")
db.close()
