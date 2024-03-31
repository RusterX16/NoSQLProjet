def get_most_popular_hashtags(db, n):
    """
    Retrieves the n most popular hashtags based on the number of unique tweets in which they are used.
    """
    # Pipeline d'agrégation pour identifier les hashtags les plus populaires.
    pipeline = [
        {"$lookup": {
            "from": "tweets",
            "localField": "idTweet",
            "foreignField": "idTweet",
            "as": "tweet_info"
        }},
        {"$unwind": "$tweet_info"},
        {"$group": {
            "_id": "$hashtag",
            "unique_tweet_count": {"$sum": 1}
        }},
        {"$sort": {"unique_tweet_count": -1}},
        {"$limit": n}
    ]

    result_cursor = db.get_collection('hashtags').aggregate(pipeline)
    return list(result_cursor)  # Retourne les résultats sous forme de liste.
