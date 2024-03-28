# ############################################################################################# #
# Question 5:                                                                                   #
# Donner le nombre d'utilisateurs différents qui ont tweeté un tweet contenant le hashtag valls #
# ############################################################################################# #
from db.mongdb import MongoDB

db = MongoDB()
hashtags_to_search = ["valls"]
initial_match = {"hashtag": {"$in": hashtags_to_search}}
results = db.aggregate_join(
    from_collection="hashtags",
    local_field="idTweet",
    foreign_collection="tweets",
    foreign_field="idTweet",
    as_field="tweet_info",
    initial_match=initial_match
)
users = set()
for result in results:
    if result['tweet_info']:
        users.add(result['tweet_info']['idUser'])
user_count = len(users)
print(f"Nombre d'utilisateurs différents qui ont twetté un tweet contenant le hashtag 'valls': {user_count}")
