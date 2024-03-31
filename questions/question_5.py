# ############################################################################################# #
# Question 5:                                                                                   #
# Donner le nombre d'utilisateurs différents qui ont tweeté un tweet contenant le hashtag valls #
# ############################################################################################# #
from db.mongodb import MongoDB
from db.neo4jdb import Neo4J

# MongoDB
db = MongoDB()
hashtags_to_search = ["valls"]
pipeline = [
    {"$match": {"hashtags": {"$in": hashtags_to_search}}},
    {"$group": {"_id": "$idUser"}},
    {"$count": "distinct_users"}
]
result = db.get_collection('tweets').aggregate(pipeline)
user_count = next(result, {}).get('distinct_users', 0)
print(f"[MongoDB] Nombre d'utilisateurs différents ayant tweeté un tweet contenant le hashtag 'valls': {user_count}")
db.close()

# Neo4J
neo = Neo4J()
query = """
MATCH (t:Tweet)-[:HAS_HASHTAG]->(h:Hashtag) 
WHERE h.name IN ['valls']
RETURN COUNT(DISTINCT t.createdBy) AS distinct_users
"""
user_count = neo.query(query)
print(f"[Neo4J] Nombre d'utilisateurs différents ayant tweeté un tweet contenant le hashtag 'valls': {user_count[0]['distinct_users']}")
neo.close()
