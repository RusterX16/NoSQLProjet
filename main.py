from neo4j import GraphDatabase
from pymongo import MongoClient
import matplotlib.pyplot as plt
import networkx as nx
import scipy as sp
import re

# Connexion à la base de données Neo4j
uri_neo4j = "neo4j+s://6c66aa85.databases.neo4j.io"
username = "neo4j"
password = "ACu8O0LLEs6te3lkqLI2XG_o0tQnZs7_w7nWflQaxbs"
neo4j_driver = GraphDatabase.driver(uri_neo4j, auth=(username, password))

# Connexion à la base de données MongoDB
client = MongoClient("mongodb://localhost:27017/")


# 1. Donner le nombre des utilisateurs;

# Avec Neo4j:
def get_neo4j_user_count(driver):
    with driver.session() as session:
        result = session.run("MATCH (n:User) RETURN count(n) as count")
        return result.single()[0]


print("Nombre d'utilisateurs dans Neo4j:", get_neo4j_user_count(neo4j_driver))

# Avec MongoDB:
db = client["NoSQL"]
collection = db["users"]
mongo_user_count = collection.count_documents({})
print("Nombre d'utilisateurs dans MongoDB:", mongo_user_count)

# Afficher les données
neo4j_user_count = get_neo4j_user_count(neo4j_driver)
mongo_user_count = mongo_user_count
labels = ['Neo4j', 'MongoDB']
counts = [neo4j_user_count, mongo_user_count]

plt.figure(figsize=(10, 6))
plt.bar(labels, counts, color=['blue', 'green'])
plt.xlabel('Base de données')
plt.ylabel('Nombre d’utilisateurs')
plt.title("Nombre d'utilisateurs dans Neo4j et MongoDB")
plt.show()


# 2. Donner le nombre des tweets;

# Avec Neo4j:
def get_neo4j_tweet_count(driver):
    with driver.session() as session:
        result = session.run("MATCH (n:Tweet) RETURN count(n) as count")
        return result.single()[0]


print("Nombre de tweets dans Neo4j:", get_neo4j_tweet_count(neo4j_driver))

# Avec MongoDB:
collection = db["tweets"]
mongo_tweet_count = collection.count_documents({})
print("Nombre de tweets dans MongoDB:", mongo_tweet_count)

# Afficher les données
neo4j_tweet_count = get_neo4j_tweet_count(neo4j_driver)
mongo_tweet_count = mongo_tweet_count
labels = ['Neo4j', 'MongoDB']
counts = [neo4j_tweet_count, mongo_tweet_count]

plt.figure(figsize=(10, 6))
plt.bar(labels, counts, color=['red', 'purple'])
plt.xlabel('Base de données')
plt.ylabel('Nombre de tweets')
plt.title("Nombre de tweets dans Neo4j et MongoDB")
plt.show()


# 3. Donner le nombre d'hastags;

# Avec Neo4j:
def get_neo4j_hashtag_count(driver):
    with driver.session() as session:
        result = session.run("MATCH (n:Hashtag) RETURN count(n) as count")
        return result.single()[0]


print("Nombre de hashtags dans Neo4j:", get_neo4j_hashtag_count(neo4j_driver))

# Avec MongoDB:
collection = db["hashtags"]
mongo_hashtag_count = collection.count_documents({})
print("Nombre de hashtags dans MongoDB:", mongo_hashtag_count)

# Afficher les données
neo4j_hashtag_count = get_neo4j_hashtag_count(neo4j_driver)
mongo_hashtag_count = mongo_hashtag_count
labels = ['Neo4j', 'MongoDB']
counts = [neo4j_hashtag_count, mongo_hashtag_count]

plt.figure(figsize=(10, 6))
plt.bar(labels, counts, color=['orange', 'brown'])
plt.xlabel('Base de données')
plt.ylabel('Nombre de hashtags')
plt.title("Nombre de hashtags dans Neo4j et MongoDB")
plt.show()


# 4. Donner le nombre de tweets contenant le hashtag "actualite";

# Avec Neo4j:
def get_neo4j_tweet_with_hashtag_count(driver, hashtag):
    with driver.session() as session:
        result = session.run(
            "MATCH (t:Tweet)-[:HAS]->(h:Hashtag) WHERE h.hashtag = $hashtag RETURN count(t) as count",
            hashtag=hashtag
        )
        return result.single()[0]


# Avec MongoDB:
def get_mongo_tweet_with_hashtag_count(db, hashtag):
    pipeline = [
        {
            '$lookup': {
                'from': "tweets",
                'localField': "idTweet",
                'foreignField': "_id",
                'as': "tweet_info"
            }
        },
        {
            '$match': {
                'Hashtag': hashtag
            }
        },
        {
            '$count': "nombre_de_tweets_avec_hashtag"
        }
    ]

    resultat = list(db["hashtags"].aggregate(pipeline))
    return resultat[0]['nombre_de_tweets_avec_hashtag'] if resultat else 0


# Affichage des données pour le hashtag 'actualite'
neo4j_count = get_neo4j_tweet_with_hashtag_count(neo4j_driver, "actualite")
mongo_count = get_mongo_tweet_with_hashtag_count(db, "actualite")
print("Nombre de tweets contenant le hashtag 'actualite' dans Neo4j:", neo4j_count)
print("Nombre de tweets contenant le hashtag 'actualite' dans MongoDB:", mongo_count)

# Afficher les données
neo4j_count_actualite = get_neo4j_tweet_with_hashtag_count(neo4j_driver, "actualite")
mongo_count_actualite = get_mongo_tweet_with_hashtag_count(db, "actualite")
labels = ['Neo4j', 'MongoDB']
counts = [neo4j_count_actualite, mongo_count_actualite]

plt.figure(figsize=(10, 6))
plt.bar(labels, counts, color=['cyan', 'magenta'])
plt.xlabel('Base de données')
plt.ylabel('Nombre de tweets (actualite)')
plt.title("Nombre de tweets contenant le hashtag 'actualite' dans Neo4j et MongoDB")
plt.show()


# 5. Donner le nombre d’utilisateurs différents qui ont tweeté un tweet contenant le hashtag valls;

# Avec Neo4j:
def get_neo4j_users_with_hashtag_count(driver, hashtag):
    with driver.session() as session:
        result = session.run(
            "MATCH (u:User)-[:TWEETE]->(t:Tweet)-[:CONTAINS]->(h:Hashtag) WHERE h.hashtag = $hashtag RETURN count(distinct u) as count",
            hashtag=hashtag
        )
        return result.single()[0]


# Avec MongoDB:
def get_mongo_users_with_hashtag_count(db, hashtag):
    pipeline = [
        {
            '$lookup': {
                'from': "tweets",  # Assurez-vous que c'est le nom correct de la collection
                'localField': "idTweet",  # Le champ dans 'hashtags' pour la jointure
                'foreignField': "_id",  # Le champ dans 'tweets' pour la jointure
                'as': "tweets_with_hashtag"
            }
        },
        {
            '$unwind': "$tweets_with_hashtag"
        },
        {
            '$group': {
                '_id': "$tweets_with_hashtag.idUser",
            }
        },
        {
            '$count': "unique_users"
        }
    ]
    resultat = list(db["hashtags"].aggregate(pipeline))
    return resultat[0]['unique_users'] if resultat else 0


# Affichage des données pour le hashtag 'valls'
neo4j_count = get_neo4j_users_with_hashtag_count(neo4j_driver, "valls")
mongo_count = get_mongo_users_with_hashtag_count(db, "valls")
print("Nombre d'utilisateurs différents ayant tweeté un tweet contenant le hashtag 'valls' dans Neo4j:", neo4j_count)
print("Nombre d'utilisateurs différents ayant tweeté un tweet contenant le hashtag 'valls' dans MongoDB:", mongo_count)

# Afficher les données
neo4j_count_valls = get_neo4j_users_with_hashtag_count(neo4j_driver, "valls")
mongo_count_valls = get_mongo_users_with_hashtag_count(db, "valls")
labels = ['Neo4j', 'MongoDB']
counts = [neo4j_count_valls, mongo_count_valls]

plt.figure(figsize=(10, 6))
plt.bar(labels, counts, color=['teal', 'lime'])
plt.xlabel('Base de données')
plt.ylabel('Nombre d’utilisateurs (valls)')
plt.title("Nombre d'utilisateurs ayant tweeté avec 'valls' dans Neo4j et MongoDB")
plt.show()


# 6.Donner les tweets qui sont des réponses à un autre tweet;

# Avec Neo4j:
def get_neo4j_reply_tweets(driver):
    with driver.session() as session:
        result = session.run(
            "MATCH (t1:Tweet)-[:REPLY_TO]->(t2:Tweet) RETURN t1.text as text1, t2.text as text2"
        )
        return result.data()


# Avec MongoDB:
def get_mongo_reply_tweets(db):
    tweets = db["tweets"]
    reply_tweets = tweets.find({"reply_to": {"$ne": None}}, {"text": 1, "reply_to": 1})
    return reply_tweets


# Affichage des données
neo4j_reply_tweets = get_neo4j_reply_tweets(neo4j_driver)
mongo_reply_tweets = list(get_mongo_reply_tweets(db))

print("Les tweets qui sont des réponses à un autre tweet dans Neo4j:"
      "\n", neo4j_reply_tweets[:5])
print("\nLes tweets qui sont des réponses à un autre tweet dans MongoDB:"
      "\n", mongo_reply_tweets[:5])

G = nx.DiGraph()

for tweet in neo4j_reply_tweets[:5]:  # Limiter le nombre de tweets pour la clarté
    G.add_node(tweet["text1"], type='original', color='skyblue')
    G.add_node(tweet["text2"], type='reply', color='lightgreen')
    G.add_edge(tweet["text1"], tweet["text2"])

for tweet in mongo_reply_tweets[:5]:  # Limiter le nombre de tweets pour la clarté
    G.add_node(tweet["text"], type='original', color='skyblue')
    G.add_node(tweet["reply_to"], type='reply', color='lightgreen')
    G.add_edge(tweet["text"], tweet["reply_to"])

pos = nx.kamada_kawai_layout(G)
node_colors = [G.nodes[n]['color'] for n in G.nodes]
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500)
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=10)
nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif")

plt.axis('off')
plt.show()


# 7. Donner le nom des followers de Spinomade (dans ce jeu de données);

# Avec Neo4j:
def get_neo4j_followers(driver, user_name):
    with driver.session() as session:
        result = session.run(
            "MATCH (u:User)-[:FOLLOWS]->(s:User {name: $user_name}) RETURN u.name AS follower",
            user_name=user_name
        )
        return [record["follower"] for record in result]


# Avec MongoDB:
def get_mongo_followers(db, screen_name):
    # Find the document for "Spinomade"
    spinomade_user_doc = db["users"].find_one({"screenName": screen_name})

    # If the user is found
    if spinomade_user_doc:
        spinomade_id = spinomade_user_doc["idUser"]

        # Find all documents in "user_follows" where Spinomade is the sourceIdUser
        followers_relations = db["user_follows"].find({"sourceIdUser": spinomade_id})
        follower_ids = [relation["targetIdUser"] for relation in followers_relations]

        # Find the usernames of all followers using their IDs
        followers = db["users"].find({"idUser": {"$in": follower_ids}})
        follower_names = [user["screenName"] for user in followers]

        return follower_names

    else:
        # If Spinomade was not found, return an empty list
        return []


# Affichage des données
neo4j_followers = get_neo4j_followers(neo4j_driver, "Spinomade")
print("Les followers de Spinomade dans Neo4j:")
print(f"Followers of Spinomade (Neo4J): {neo4j_followers}")
screen_name = "Spinomade"  # Replace with the actual screen name used in the users collection
followers_of_spinomade = get_mongo_followers(db, screen_name)
print(f"Followers of Spinomade (MongoDB): {followers_of_spinomade}")


# 8. Donner le nom des utilisateurs suivis par Spinomade (dans ce jeu de données);

# Avec Neo4j:
def get_neo4j_following(driver, user_name):
    with driver.session() as session:
        result = session.run(
            "MATCH (s:User {name: $user_name})-[:FOLLOWS]->(u:User) RETURN u.name AS following",
            user_name=user_name
        )
        return [record["following"] for record in result]


# Avec MongoDB:
def get_mongo_following(db, screen_name):
    # Find the document for "Spinomade"
    spinomade_user_doc = db["users"].find_one({"screenName": screen_name})

    # If the user is found
    if spinomade_user_doc:
        spinomade_id = spinomade_user_doc["idUser"]

        # Find all documents in "user_follows" where Spinomade is the targetIdUser
        following_relations = db["user_follows"].find({"targetIdUser": spinomade_id})
        following_ids = [relation["sourceIdUser"] for relation in following_relations]

        # Find the usernames of all users followed by Spinomade using their IDs
        following = db["users"].find({"idUser": {"$in": following_ids}})
        following_names = [user["screenName"] for user in following]

        return following_names

    else:
        # If Spinomade was not found, return an empty list
        return []


# Affichage des données
neo4j_following = get_neo4j_following(neo4j_driver, "Spinomade")
print("Les utilisateurs suivis par Spinomade dans Neo4j:")
print(f"Following of Spinomade (Neo4J): {neo4j_following}")
following_of_spinomade = get_mongo_following(db, "Spinomade")
print(f"Following of Spinomade (MongoDB): {following_of_spinomade}")


# 9. Donner le nom des utilisateurs qui sont `a la fois followers et followees de Spinomade;

# Avec Neo4j:
def get_neo4j_mutual_followers(driver, user_name):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (a:User)-[:FOLLOWS]->(s:User {name: $user_name}), 
                  (s)-[:FOLLOWS]->(a)
            RETURN a.name AS mutual
            """,
            user_name=user_name
        )
        return [record["mutual"] for record in result]


# Avec MongoDB:
def get_mongo_mutual_followers(db, screen_name):
    # Find the document for "Spinomade"
    spinomade_user_doc = db["users"].find_one({"screenName": screen_name})

    # If the user is found
    if spinomade_user_doc:
        spinomade_id = spinomade_user_doc["idUser"]

        # Find all documents in "user_follows" where Spinomade is the sourceIdUser
        followers_relations = db["user_follows"].find({"sourceIdUser": spinomade_id})
        follower_ids = [relation["targetIdUser"] for relation in followers_relations]

        # Find all documents in "user_follows" where Spinomade is the targetIdUser
        following_relations = db["user_follows"].find({"targetIdUser": spinomade_id})
        following_ids = [relation["sourceIdUser"] for relation in following_relations]

        # Find the usernames of all users who are both followers and followees of Spinomade
        mutual_ids = set(follower_ids).intersection(following_ids)
        mutual_users = db["users"].find({"idUser": {"$in": list(mutual_ids)}})
        mutual_names = [user["screenName"] for user in mutual_users]

        return mutual_names

    else:
        # If Spinomade was not found, return an empty list
        return []


# Affichage des données
neo4j_mutual_followers = get_neo4j_mutual_followers(neo4j_driver, "Spinomade")
mutual_followers = get_neo4j_mutual_followers(neo4j_driver, "Spinomade")
print("Mutual followers of Spinomade (Neo4J):", mutual_followers)
mutual_followers_of_spinomade = get_mongo_mutual_followers(db, "Spinomade")
print(f"Mutual followers of Spinomade (MongoDB): {mutual_followers_of_spinomade}")


# 10. Donner les utilisateurs ayant plus de 10 followers (dans ce jeu de données);

# Avec Neo4j:
def get_neo4j_users_with_more_than_10_followers(driver, min_followers):
    with driver.session() as session:
        result = session.run(
            "MATCH (u:User)-[:FOLLOWS]->(f:User) WITH u, count(f) as followers WHERE followers > $min_followers RETURN u.name AS user",
            min_followers=min_followers
        )
        return [record["user"] for record in result]


# Avec MongoDB:
def get_mongo_users_with_more_than_10_followers(db, min_followers):
    pipeline = [
        {
            '$lookup': {
                'from': "user_follows",
                'localField': "idUser",
                'foreignField': "targetIdUser",
                'as': "followers"
            }
        },
        {
            '$addFields': {
                'follower_count': {'$size': "$followers"}
            }
        },
        {
            '$match': {
                'follower_count': {'$gt': min_followers}
            }
        },
        {
            '$project': {
                'screenName': 1
            }
        }
    ]

    result = list(db["users"].aggregate(pipeline))
    return [user["screenName"] for user in result]


# Affichage des données
min_followers = 10

neo4j_users = get_neo4j_users_with_more_than_10_followers(neo4j_driver, min_followers)
mongo_users = get_mongo_users_with_more_than_10_followers(db, min_followers)

neo4j_count = len(neo4j_users)
mongo_count = len(mongo_users)

labels = ['Neo4j', 'MongoDB']
counts = [neo4j_count, mongo_count]

plt.figure(figsize=(8, 6))
plt.bar(labels, counts, color=['blue', 'green'])

plt.title('Users with More Than 10 Followers')
plt.xlabel('Database')
plt.ylabel('Number of Users')

plt.show()


# 11. Donner les utilisateurs qui follows plus de 5 utilisateurs (dans ce jeu de données);

# Avec Neo4j:
def get_neo4j_users_following_more_than_5_users(driver, min_following):
    with driver.session() as session:
        result = session.run(
            "MATCH (u:User)-[:FOLLOWS]->(f:User) WITH u, count(f) as following WHERE following > $min_following "
            "RETURN u.name AS user",
            min_following=min_following
        )
        return [record["user"] for record in result]


# Avec MongoDB:
def get_mongo_users_following_more_than_5_users(db, min_following):
    pipeline = [
        {
            '$lookup': {
                'from': "user_follows",
                'localField': "idUser",
                'foreignField': "sourceIdUser",
                'as': "following"
            }
        },
        {
            '$addFields': {
                'following_count': {'$size': "$following"}
            }
        },
        {
            '$match': {
                'following_count': {'$gt': min_following}
            }
        },
        {
            '$project': {
                'screenName': 1
            }
        }
    ]

    result = list(db["users"].aggregate(pipeline))
    return [user["screenName"] for user in result]


# Affichage des données
min_following = 5

neo4j_users = get_neo4j_users_following_more_than_5_users(neo4j_driver, min_following)
mongo_users = get_mongo_users_following_more_than_5_users(db, min_following)

neo4j_count = len(neo4j_users)
mongo_count = len(mongo_users)

labels = ['Neo4j', 'MongoDB']
counts = [neo4j_count, mongo_count]

plt.figure(figsize=(8, 6))
plt.bar(labels, counts, color=['blue', 'green'])

plt.title('Users Following More Than 5 Users')
plt.xlabel('Database')
plt.ylabel('Number of Users')

plt.show()


# 12.Donner les 10 tweets les plus populaires (i.e la popularité se mesure au nombre de fois où le tweet est favori.)

# Avec Neo4j:

def get_neo4j_most_popular_tweets(driver, limit):
    with driver.session() as session:
        result = session.run(
            "MATCH (t:Tweet) RETURN t.text AS text, t.nbfavorites AS favorites ORDER BY favorites DESC LIMIT $limit",
            limit=limit
        )
        return [(record["text"], record["favorites"]) for record in result]


# Avec MongoDB:
def get_mongo_most_popular_tweets(db, limit):
    pipeline = [
        {
            '$sort': {'nbfavorites': -1}
        },
        {
            '$limit': limit
        },
        {
            '$project': {'text': 1, 'nbfavorites': 1}
        }
    ]

    result = list(db.tweets.aggregate(pipeline))
    return [(tweet.get("text", "No text available"), tweet.get("nbfavorites", 0)) for tweet in result]


neo4j_tweets = get_neo4j_most_popular_tweets(neo4j_driver, 10)
mongo_tweets = get_mongo_most_popular_tweets(db, 10)

# Affichage des données
print("Les 10 tweets les plus populaires dans Neo4j:")
for i, (text, favorites) in enumerate(neo4j_tweets, start=1):
    print(f"{i}. {text} - {favorites} favorites")

print("\nLes 10 tweets les plus populaires dans MongoDB:")
for i, (text, favorites) in enumerate(mongo_tweets, start=1):
    print(f"{i}. {text} - {favorites} favorites")

# Handling empty result sets
if neo4j_tweets:
    neo4j_texts, neo4j_favorites = zip(*neo4j_tweets)
else:
    neo4j_texts, neo4j_favorites = [], []

if mongo_tweets:
    mongo_texts, mongo_favorites = zip(*mongo_tweets)
else:
    mongo_texts, mongo_favorites = [], []

plt.figure(figsize=(12, 6))

# Ensure there are tweets to display
if neo4j_texts:
    plt.barh(range(len(neo4j_texts)), neo4j_favorites, color='blue', label='Neo4j')
if mongo_texts:
    plt.barh(range(len(mongo_texts)), mongo_favorites, color='green', label='MongoDB', left=neo4j_favorites)

plt.yticks(range(len(neo4j_texts) + len(mongo_texts)), list(neo4j_texts) + list(mongo_texts))
plt.xlabel('Number of Favorites')
plt.title('Top 10 Most Popular Tweets')
plt.legend()
plt.tight_layout()
plt.show()


# 13. Donner les 10 hashtags les plus populaires (i.e. la popularité se mesure au nombre de tweets dans lesquels ils apparaissent.);

# Avec Neo4j:

def get_neo4j_most_popular_hashtags(driver, limit):
    with driver.session() as session:
        result = session.run(
            "MATCH (h:Hashtag)<-[:CONTAINS]-(t:Tweet) RETURN h.hashtag AS hashtag, count(t) AS tweet_count "
            "ORDER BY tweet_count DESC LIMIT $limit",
            limit=limit
        )
        return [(record["hashtag"], record["tweet_count"]) for record in result]


# Avec MongoDB:
def get_mongo_most_popular_hashtags(db, limit):
    pipeline = [
        {
            '$unwind': "$Hashtag"
        },
        {
            '$group': {
                '_id': "$Hashtag",
                'tweet_count': {'$sum': 1}
            }
        },
        {
            '$sort': {'tweet_count': -1}
        },
        {
            '$limit': limit
        }
    ]

    result = list(db.tweets.aggregate(pipeline))
    return [(hashtag["_id"], hashtag["tweet_count"]) for hashtag in result]


neo4j_hashtags = get_neo4j_most_popular_hashtags(neo4j_driver, 10)
mongo_hashtags = get_mongo_most_popular_hashtags(db, 10)

# Extracting labels (hashtags) and values (tweet counts) from the query results
neo4j_labels, neo4j_values = zip(*neo4j_hashtags) if neo4j_hashtags else ([], [])
mongo_labels, mongo_values = zip(*mongo_hashtags) if mongo_hashtags else ([], [])

# Calculate indices for each hashtag to use in plotting
indices = range(len(neo4j_labels))

# Plotting
plt.figure(figsize=(14, 7))
bar_width = 0.35  # Width of the bars

# Check if there is Neo4j data available before plotting
if neo4j_labels and neo4j_values:
    plt.bar(indices, neo4j_values, bar_width, label='Neo4j')

# Adjust indices for MongoDB data if both datasets are available
if mongo_labels and mongo_values:
    mongo_indices = [i + bar_width for i in indices][:len(mongo_labels)]  # Adjust if lengths differ
    plt.bar(mongo_indices, mongo_values, bar_width, label='MongoDB', color='orange')

# Adding title and labels
plt.xlabel('Hashtags')
plt.ylabel('Tweet Count')
plt.title('Top 10 Most Popular Hashtags')

# Adjusting the x-ticks to show labels more clearly
# Ensure we have labels before attempting to set xticks
if neo4j_labels:
    plt.xticks([i + bar_width / 2 for i in indices][:len(neo4j_labels)], neo4j_labels, rotation=45, ha="right")

# Adding legend
plt.legend()

# Showing the plot
plt.tight_layout()
plt.show()


# 14. Donner les tweets qui initient une discussion (i.e. une discussion est un enchaînement de tweets deux à deux reliés par un lien de type REPLY TO);

# Avec Neo4j:

def get_neo4j_discussions(driver):
    with driver.session() as session:
        result = session.run(
            "MATCH (t1:Tweet)-[:REPLY_TO*]->(t2:Tweet) WHERE NOT (t2)-[:REPLY_TO]->() RETURN t1.text AS text1, t2.text AS text2"
        )
        return result.data()


# Avec MongoDB:
def get_mongo_discussions(db):
    tweets = db["tweets"]
    discussions = tweets.find({"reply_to": {"$ne": None}}, {"text": 1, "reply_to": 1})
    return discussions


# Affichage des données
neo4j_discussions = get_neo4j_discussions(neo4j_driver)
mongo_discussions = list(get_mongo_discussions(db))

print("Les tweets qui initient une discussion dans Neo4j:"
      "\n", neo4j_discussions[:5])
print("\nLes tweets qui initient une discussion dans MongoDB:"
      "\n", mongo_discussions[:5])

G = nx.DiGraph()

for tweet in neo4j_discussions[:5]:  # Limiter le nombre de tweets pour la clarté
    G.add_node(tweet["text1"], type='original', color='skyblue')
    G.add_node(tweet["text2"], type='reply', color='lightgreen')
    G.add_edge(tweet["text1"], tweet["text2"])

for tweet in mongo_discussions[:5]:  # Limiter le nombre de tweets pour la clarté
    G.add_node(tweet["text"], type='original', color='skyblue')
    G.add_node(tweet["reply_to"], type='reply', color='lightgreen')
    G.add_edge(tweet["text"], tweet["reply_to"])

pos = nx.kamada_kawai_layout(G)
node_colors = [G.nodes[n]['color'] for n in G.nodes]
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500)
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=10)
nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif")

plt.axis('off')
plt.show()


# 15. Quelle est la plus longue discussion ?

# Avec Neo4j:

def get_neo4j_longest_discussion(driver):
    with driver.session() as session:
        result = session.run(
            """
            MATCH path=(t1:Tweet)-[:REPLY_TO*]->(t2:Tweet)
            WHERE NOT (t2)-[:REPLY_TO]->()
            WITH t1, t2, length(path) AS discussion_length
            RETURN t1.text AS text1, t2.text AS text2, discussion_length
            ORDER BY discussion_length DESC LIMIT 1
            """
        )
        return result.single()


# Avec MongoDB:

def get_mongo_longest_discussion(db):
    pipeline = [
        {
            '$match': {
                'replyToTweet': {'$exists': True}  # Assurez-vous que le champ 'replyToTweet' existe.
            }
        },
        {
            '$graphLookup': {  # Utilisez $graphLookup pour résoudre la chaîne de réponses
                'from': "tweets",  # La collection à partir de laquelle effectuer la recherche
                'startWith': "$replyToTweet",  # Le champ qui contient la référence au tweet parent
                'connectFromField': "replyToTweet",  # Le champ par lequel continuer la recherche
                'connectToField': "_id",  # Le champ dans les documents parents à comparer avec connectFromField
                'as': "chain",  # Le nom du tableau dans lequel les résultats correspondants seront stockés
                'depthField': "depth"
                # Un champ qui sera ajouté à chaque document du tableau "chain" pour indiquer la profondeur de la chaîne
            }
        },
        {
            '$sort': {'depth': -1}  # Triez les résultats par la profondeur, décroissante
        },
        {
            '$limit': 1  # Limitez le résultat à la chaîne de discussion la plus longue
        }
    ]

    longest_discussion = list(db.tweets.aggregate(pipeline))
    return longest_discussion[0] if longest_discussion else None


# Affichage des données
neo4j_longest_discussion = get_neo4j_longest_discussion(neo4j_driver)
mongo_longest_discussion = get_mongo_longest_discussion(db)

print("La plus longue discussion dans Neo4j:")
print(neo4j_longest_discussion)
print("\nLa plus longue discussion dans MongoDB:")
print(mongo_longest_discussion)


# 16. Pour chaque conversation, donnez-en le début et la fin.

# Avec Neo4j:

def get_neo4j_discussion_start_end(driver):
    with driver.session() as session:
        result = session.run(
            """
            MATCH path=(t1:Tweet)-[:REPLY_TO*]->(t2:Tweet)
            WHERE NOT (t2)-[:REPLY_TO]->()
            WITH t1, t2, length(path) AS discussion_length
            RETURN t1.text AS start, t2.text AS end
            """
        )
        return result.data()


# Avec MongoDB:

def get_mongo_discussion_start_end(db):
    pipeline = [
        {
            '$match': {
                'replyToTweet': {
                    '$exists': True
                }
            }
        },
        {
            '$graphLookup': {
                'from': "tweets",
                'startWith': "$replyToTweet",
                'connectFromField': "replyToTweet",
                'connectToField': "_id",
                'as': "chain",
                'depthField': "depth"
            }
        },
        {
            '$sort': {
                'depth': -1
            }
        },
        {
            '$project': {
                'start': {
                    '$arrayElemAt': ["$chain.text", -1]
                },
                'end': "$text"
            }
        }
    ]

    discussions = list(db.tweets.aggregate(pipeline))

    return discussions


# Affichage des données
neo4j_discussions = get_neo4j_discussion_start_end(neo4j_driver)
mongo_discussions = get_mongo_discussion_start_end(db)

print("Les débuts et fins de chaque conversation dans Neo4j:")
for i, discussion in enumerate(neo4j_discussions, start=1):
    print(f"{i}. Start: {discussion['start']}, End: {discussion['end']}")

print("\nLes débuts et fins de chaque conversation dans MongoDB:")
for i, discussion in enumerate(mongo_discussions, start=1):
    print(f"{i}. Start: {discussion['start']}, End: {discussion['end']}")

# Assuming `discussion_length` is available in your results
neo4j_lengths = [len(disc['start']) + len(disc['end']) for disc in
                 neo4j_discussions]  # This is a placeholder for actual length
mongo_lengths = [len(disc['start']) + len(disc['end']) for disc in
                 mongo_discussions]  # This is a placeholder for actual length

indices = range(len(neo4j_lengths))
bar_width = 0.35

plt.figure(figsize=(14, 7))

# Plot Neo4j data
plt.bar(indices, neo4j_lengths, bar_width, label='Neo4j', color='blue')

# Check if MongoDB returned any data and plot if it did
if mongo_lengths:
    plt.bar([i + bar_width for i in indices], mongo_lengths, bar_width, label='MongoDB', color='orange')
else:
    print("No discussion length data returned from MongoDB.")

plt.xlabel('Conversation Index')
plt.ylabel('Discussion Length')
plt.title('Discussion Lengths in Neo4j and MongoDB')
plt.legend()

plt.tight_layout()
plt.show()
