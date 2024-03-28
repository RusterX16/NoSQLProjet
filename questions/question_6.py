# ######################################################## #
# Question 6:                                              #
# Donner les tweets qui sont des réponses à un autre tweet #
# ######################################################## #
from db.mongdb import MongoDB

db = MongoDB()
initial_match = {"replyIdTweet": {"$ne": None}}
results = db.get('tweets', initial_match)

for i, result in enumerate(results):
    print(f"[{i+1}] {result['idTweet']}: {result['text']}")
