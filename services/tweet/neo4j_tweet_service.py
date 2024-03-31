def get_most_popular_tweets(db, n):
    """
    Retrieve the n most popular tweets by the number of times they have been favorited in Neo4j.
    """
    query = """
    MATCH (t:Tweet)
    WHERE t.nbfavorites IS NOT NULL
    RETURN t.id AS idTweet, t.text AS text, toInteger(t.nbfavorites) AS nbFavorites
    ORDER BY nbFavorites DESC
    LIMIT $n
    """
    results = db.query(query, params={"n": n})

    if not results:
        print("No results were returned from the query.")
        return []

    return [{
        'idTweet': record['idTweet'],
        'text': record['text'],
        'nbFavorites': record['nbFavorites']
    } for record in results if record['idTweet'] is not None and record['nbFavorites'] is not None]
