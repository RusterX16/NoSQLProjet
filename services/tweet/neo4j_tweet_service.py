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
