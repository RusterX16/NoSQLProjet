def get_reply_tweets(db):
    query = "MATCH (t:Tweet) WHERE t.replyIdTweet IS NOT NULL RETURN t"
    results = db.query(query)
    return [record['t'] for record in results]  # Adjusted to fetch the 't' property from each record


def get_most_popular_tweets(db, n):
    query = """
    MATCH (t:Tweet)
    WHERE t.nbfavorites IS NOT NULL
    RETURN t.idTweet AS idTweet, t.text AS text, toInteger(t.nbfavorites) AS nbFavorites
    ORDER BY nbFavorites DESC
    LIMIT $n
    """
    results = db.query(query, params={"n": n})
    return [record for record in results]
