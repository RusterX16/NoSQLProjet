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
