# ###################################### #
# Question 15:                           #
# Quelle est la plus longue discussion ? #
# ###################################### #
from services.tweet.mongodb_tweet_service import find_longest_thread
from db.neo4jdb import Neo4J
from db.mongdb import MongoDB

db = MongoDB()
longest_thread = find_longest_thread(db)
print("[MongoDB] Longest discussion:")

if longest_thread:
    discussion = longest_thread[0]  # Assuming the result is a list with one entry
    depth = discussion['numberOfReplies']
    thread = discussion['thread']
    print(f"Depth: {depth}")

    for i, tweet in enumerate(thread):
        text = tweet.get('text', '[No text available]')
        createdAt = tweet.get('createdAt', '[No date available]')
        tweetDepth = tweet.get('depth', '[No depth available]')
        print(f"[{tweetDepth}] {createdAt}: {text}")
else:
    print("No discussion found.")

db.close()

neo = Neo4J()
query = """
    MATCH p=(t:Tweet)-[:REPLY_TO*]->(reply:Tweet)
    WITH p, length(p) AS depth
    ORDER BY depth DESC
    LIMIT 1
    UNWIND nodes(p) AS tweet
    RETURN tweet.text AS text, depth
    """
results = neo.query(query)
print("[Neo4J] Longest discussion:")
depth = None

for i, record in enumerate(results):
    if depth is None:  # Just set the depth once.
        depth = record['depth']
        print(f"Depth: {depth}")

    if i == 0:
        print(f"[Root tweet] {record['text']}")
        continue
    print(f"[{i - 1}] {record['text']}")

neo.close()
