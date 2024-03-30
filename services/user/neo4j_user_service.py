def get_followers_by_user(db, name):
    query = "MATCH (u:User)<-[:FOLLOWS]-(f:User) WHERE u.name = $username RETURN f.name AS name"
    results = db.query(query, params={"username": name})
    return [record["name"] for record in results]


def get_followings_by_user(db, name):
    query = "MATCH (u:User {name: $username})-[:FOLLOWS]->(following:User) RETURN following.name AS name"
    results = db.query(query, params={"username": name})
    return [record["name"] for record in results]


def get_mutual_by_user(db, name):
    followers = set(get_followers_by_user(db, name))
    followings = set(get_followings_by_user(db, name))

    return list(followers.intersection(followings))


def get_users_names_with_more_than_n_followers(db, n):
    query = "MATCH (u:User) WHERE size([(u)<-[:FOLLOWS]-() | 1]) > $n RETURN u.name AS name"
    results = db.query(query, params={"n": n})
    return [record["name"] for record in results]


def get_users_names_with_more_than_n_followings(db, n):
    # Using pattern comprehension to count followees
    query = """
    MATCH (u:User)
    WHERE size([(u)-[:FOLLOWS]->(f) | f]) > $n
    RETURN u.name AS name
    """
    results = db.query(query, params={"n": n})
    return [record["name"] for record in results]

