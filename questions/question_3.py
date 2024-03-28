# ########################### #
# Question 3:                 #
# Donner le nombre d'hashtags #
# ########################### #
from db.mongdb import MongoDB

db = MongoDB()
hashtag_count = (db.count('hashtags'))
print(f"[MongoDB] Nombre d'hashtags: {hashtag_count}")
