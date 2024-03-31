def get_tweet_text_by_id(db, id_tweet):
    """
    Retrieve the text of a tweet by its ID.
    """
    # Recherche du tweet par son ID et retourne uniquement le texte.
    tweet = db.get_collection('tweets').find_one({"idTweet": id_tweet}, {"text": 1})
    return tweet['text'] if tweet else None  # Retourne le texte si le tweet est trouvé.


def get_most_popular_tweets(db, n):
    """
    Retrieve the n most popular tweets by the number of times they have been favorited in MongoDB.
    """
    pipeline = [
        {"$match": {"nbFavorites": {"$exists": True, "$type": "int"}}},  # Ensure nbFavorites is an integer
        {"$sort": {"nbFavorites": -1}},
        {"$limit": n},
        {"$project": {"_id": 1, "text": 1, "nbFavorites": 1}}
    ]
    results = db.get_collection('tweets').aggregate(pipeline)
    return list(results)


def find_longest_thread(db):
    # Pipeline pour identifier la chaîne de tweets (thread) la plus longue.
    pipeline = [
        {
            "$match": {
                "replyIdTweet": {"$exists": True}  # Commence avec les tweets qui sont des réponses.
            }
        },
        {
            "$graphLookup": {  # Construction du thread de réponses.
                "from": "tweets",
                "startWith": "$replyIdTweet",
                "connectFromField": "replyIdTweet",
                "connectToField": "idTweet",
                "as": "thread",
                "depthField": "depth"
            }
        },
        {
            "$project": {  # Projection des champs nécessaires, incluant la taille du thread.
                "text": 1,
                "thread": 1,
                "numberOfReplies": {"$size": "$thread"}
            }
        },
        {"$sort": {"numberOfReplies": -1}},  # Tri pour obtenir la discussion la plus longue.
        {"$limit": 1}  # Limite au premier résultat, le plus long thread.
    ]

    return list(db.get_collection('tweets').aggregate(pipeline))
