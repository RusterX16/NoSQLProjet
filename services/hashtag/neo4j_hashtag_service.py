def get_most_popular_hashtags(db, n):
    """
    Retrieve the n most popular hashtags based on the count of tweets that contain them in Neo4j.
    """
    # Requête Cypher pour récupérer les 'n' hashtags les plus populaires basés sur leur présence dans les tweets.
    query = """
    MATCH (h:Hashtag)<-[:CONTAINS]-(t:Tweet)
    RETURN h.hashtag AS hashtag, COUNT(t) AS tweetCount
    ORDER BY tweetCount DESC
    LIMIT $n
    """
    results = db.query(query, params={"n": n})
    return [record for record in results]  # Retourne une liste de résultats.
