def get_follower_screennames_by_user_id(db, user_id):
    """
    Retrieve the screen names of all followers of a given user by the user's ID.

    Assumes 'user_follows' collection contains documents with 'sourceIdUser' and 'targetIdUser'.
    Assumes 'users' collection contains 'idUser' and 'screenName'.
    """
    followers_pipeline = [
        {"$match": {"sourceIdUser": user_id}},
        {"$lookup": {
            "from": "users",  # Join with the 'users' collection
            "localField": "targetIdUser",  # Field from 'user_follows' collection
            "foreignField": "idUser",  # Field from 'users' collection
            "as": "follower_data"
        }},
        {"$unwind": "$follower_data"},  # Deconstruct 'follower_data' array
        {"$project": {"screenName": "$follower_data.screenName"}}  # Project the 'screenName' field
    ]

    # Run the aggregation pipeline
    follower_screennames = [
        doc['screenName'] for doc in db.get_collection('user_follows').aggregate(followers_pipeline)
    ]

    return follower_screennames


def get_following_screennames_by_user_id(db, user_id):
    """
    Retrieve the screen names of all users followed by a given user by the user's ID.

    Assumes 'user_follows' collection contains documents with 'sourceIdUser' and 'targetIdUser'.
    Assumes 'users' collection contains 'idUser' and 'screenName'.
    """
    following_pipeline = [
        {"$match": {"targetIdUser": user_id}},
        {"$lookup": {
            "from": "users",  # Join with the 'users' collection
            "localField": "sourceIdUser",  # Field from 'user_follows' collection
            "foreignField": "idUser",  # Field from 'users' collection
            "as": "following_data"
        }},
        {"$unwind": "$following_data"},  # Deconstruct 'following_data' array
        {"$project": {"screenName": "$following_data.screenName"}}  # Project the 'screenName' field
    ]

    # Run the aggregation pipeline
    following_screennames = [
        doc['screenName'] for doc in db.get_collection('user_follows').aggregate(following_pipeline)
    ]

    return following_screennames


def get_mutual_screennames_by_user_id(db, user_id):
    """
    Retrieve the screen names of all users who are both followers and followees of a given user by the user's ID.

    Assumes 'user_follows' collection contains documents with 'sourceIdUser' and 'targetIdUser'.
    Assumes 'users' collection contains 'idUser' and 'screenName'.
    """
    followers = set(get_follower_screennames_by_user_id(db, user_id))
    followings = set(get_following_screennames_by_user_id(db, user_id))
    mutual_screennames = list(followers.intersection(followings))

    return mutual_screennames


def get_users_screennames_with_more_than_n_followers(db, n):
    """
    Retrieve the screen names of users who have more than 'n' followers.

    Assumes 'user_follows' collection contains documents with 'sourceIdUser' and 'targetIdUser'.
    Assumes 'users' collection contains 'idUser' and 'screenName'.
    """
    followers_count_pipeline = [
        {"$group": {"_id": "$targetIdUser", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": n}}},
        {"$lookup": {
            "from": "users",  # Join with the 'users' collection
            "localField": "_id",  # Field from 'followers_count' collection
            "foreignField": "idUser",  # Field from 'users' collection
            "as": "user_data"
        }},
        {"$unwind": "$user_data"},  # Deconstruct 'user_data' array
        {"$project": {"screenName": "$user_data.screenName"}}  # Project the 'screenName' field
    ]

    # Run the aggregation pipeline
    users_screennames = [
        doc['screenName'] for doc in db.get_collection('user_follows').aggregate(followers_count_pipeline)
    ]

    return users_screennames

def get_users_screennames_with_more_than_n_followings(db, n):
    """
    Retrieve the screen names of users who follow more than 'n' users.

    Assumes 'user_follows' collection contains documents with 'sourceIdUser' and 'targetIdUser'.
    Assumes 'users' collection contains 'idUser' and 'screenName'.
    """
    followees_count_pipeline = [
        {"$group": {"_id": "$sourceIdUser", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": n}}},
        {"$lookup": {
            "from": "users",  # Join with the 'users' collection
            "localField": "_id",  # Field from 'followees_count' collection
            "foreignField": "idUser",  # Field from 'users' collection
            "as": "user_data"
        }},
        {"$unwind": "$user_data"},  # Deconstruct 'user_data' array
        {"$project": {"screenName": "$user_data.screenName"}}  # Project the 'screenName' field
    ]

    # Run the aggregation pipeline
    users_screennames = [
        doc['screenName'] for doc in db.get_collection('user_follows').aggregate(followees_count_pipeline)
    ]

    return users_screennames
