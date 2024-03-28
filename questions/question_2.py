# ########################## #
# Question 2:                #
# Donner le nombre de tweets #
# ########################## #
from db.mongdb import MongoDB

db = MongoDB()
tweet_count = db.count('tweets')
print(f"[MongoDB] Nombre de tweets: {tweet_count}")
