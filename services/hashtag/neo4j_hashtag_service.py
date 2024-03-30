def get_most_popular_hashtags(db, n):
    query = """
    MATCH (h:Hashtag)<-[:CONTAINS]-(t:Tweet)
    RETURN h.hashtag AS hashtag, COUNT(t) AS tweetCount
    ORDER BY tweetCount DESC
    LIMIT $n
    """
    results = db.query(query, params={"n": n})
    return [record for record in results]

