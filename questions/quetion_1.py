# ############################### #
# Question 1:                     #
# Donner le nombre d'utilisateurs #
# ############################### #
from db.mongdb import MongoDB

db = MongoDB()
user_count = db.count('users')
print(f"[MongoDB] Nombre d'utilisateur: {user_count}")
