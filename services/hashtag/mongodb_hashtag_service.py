def get_most_popular_hashtags(db, n):
    """
    Retrieves the n most popular hashtags based on the number of unique tweets in which they are used.
    Assumes that 'idTweet' in 'hashtags' is an integer referencing a similar field in 'tweets'.
    """
    pipeline = [
        {"$lookup": {
            "from": "tweets",  # The collection to join with
            "localField": "idTweet",  # Field from the hashtags collection
            "foreignField": "idTweet",  # Corresponding integer field in the tweets collection
            "as": "tweet_info"  # The output array field with joined tweet information
        }},
        {"$unwind": "$tweet_info"},  # Deconstruct the tweet_info array
        {"$group": {
            "_id": "$hashtag",
            "unique_tweet_count": {"$sum": 1}
        }},
        {"$sort": {"unique_tweet_count": -1}},  # Sort by the count in descending order
        {"$limit": n}
    ]

    result_cursor = db.get_collection('hashtags').aggregate(pipeline)
    return list(result_cursor)
