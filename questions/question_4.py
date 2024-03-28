# ######################################################### #
# Question 4:                                               #
# Donner le nombre de tweets contenant le hashtag actualité #
# ######################################################### #
from db.mongdb import MongoDB

db = MongoDB()
hashtags_to_search = ["actualité", "actualite"]
initial_match = {"hashtag": {"$in": hashtags_to_search}}
results = db.aggregate_join(
    from_collection="hashtags",
    local_field="idTweet",
    foreign_collection="tweets",
    foreign_field="idTweet",
    as_field="tweet_info",
    initial_match=initial_match
)
tweet_count = sum(1 for _ in results if _['tweet_info'])
print(f"Nombre de tweets contenant 'actualité' ou 'actualite': {tweet_count}")
