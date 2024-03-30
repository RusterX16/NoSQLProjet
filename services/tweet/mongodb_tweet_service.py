def get_tweet_text_by_id(db, id_tweet):
    """
    Retrieve the text of a tweet by its ID.

    Assumes 'tweets' collection contains documents with 'idTweet'.
    """
    tweet = db.get_collection('tweets').find_one({"idTweet": id_tweet}, {"text": 1})
    return tweet['text'] if tweet else None


def get_most_popular_tweets(db, n):
    """
    Retrieve the n most popular tweets by the number of times they have been favorited.

    Assumes 'tweets' collection contains documents with 'favoriteCount'.
    """
    most_popular_pipeline = [
        {"$sort": {"nbFavorites": -1}},  # Sort by 'favoriteCount' in descending order
        {"$limit": n},  # Limit to n results
        {"$project": {"idTweet": 1, "text": 1, "nbFavorites": 1}}  # Include 'favoriteCount' in the results
    ]

    # Run the aggregation pipeline
    result_cursor = db.get_collection('tweets').aggregate(most_popular_pipeline)
    most_popular_tweets = [doc for doc in result_cursor]

    return most_popular_tweets


def find_longest_thread(db):
    pipeline = [
        # On commence par les tweets qui ont un replyIdTweet
        {
            "$match": {
                "replyIdTweet": {"$exists": True}
            }
        },
        # On construit la chaîne de réponses pour chaque tweet
        {
            "$graphLookup": {
                "from": "tweets",
                "startWith": "$replyIdTweet",
                "connectFromField": "replyIdTweet",
                "connectToField": "idTweet",
                "as": "thread",
                "depthField": "depth"
            }
        },
        # On projette les informations nécessaires
        {
            "$project": {
                "text": 1,
                "thread": 1,
                "numberOfReplies": {"$size": "$thread"}
            }
        },
        # On trie pour obtenir la plus longue discussion
        {
            "$sort": {"numberOfReplies": -1}
        },
        # On ne prend que la première (la plus longue)
        {
            "$limit": 1
        }
    ]

    return list(db.get_collection('tweets').aggregate(pipeline))
