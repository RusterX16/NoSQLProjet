def get_reply_tweets(db):
    query = "MATCH (t:Tweet) WHERE t.replyIdTweet IS NOT NULL RETURN t"
    results = db.query(query)
    return [record['t'] for record in results]  # Adjusted to fetch the 't' property from each record
