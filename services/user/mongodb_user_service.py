def get_follower_screennames_by_user_id(db, user_id):
    """
    Récupère les noms d'écran de tous les abonnés d'un utilisateur donné par l'ID de l'utilisateur.
    """
    followers_pipeline = [
        {"$match": {"targetIdUser": user_id}},
        {"$lookup": {
            "from": "users",
            "localField": "sourceIdUser",
            "foreignField": "idUser",
            "as": "follower_data"
        }},
        {"$unwind": "$follower_data"},
        {"$project": {"screenName": "$follower_data.screenName"}}
    ]

    follower_screennames = [
        doc['screenName'] for doc in db.get_collection('user_follows').aggregate(followers_pipeline)
    ]

    return follower_screennames


def get_following_screennames_by_user_id(db, user_id):
    """
    Récupère les noms d'écran de tous les utilisateurs suivis par un utilisateur donné par l'ID de l'utilisateur.
    """
    following_pipeline = [
        {"$match": {"sourceIdUser": user_id}},
        {"$lookup": {
            "from": "users",
            "localField": "targetIdUser",
            "foreignField": "idUser",
            "as": "following_data"
        }},
        {"$unwind": "$following_data"},
        {"$project": {"screenName": "$following_data.screenName"}}
    ]

    following_screennames = [
        doc['screenName'] for doc in db.get_collection('user_follows').aggregate(following_pipeline)
    ]

    return following_screennames


def get_mutual_screennames_by_user_id(db, user_id):
    """
    Retrieve the screen names of all users who are both followers and followees of a given user by the user's ID.
    """
    # Utilisation des fonctions précédentes pour calculer les noms d'écran mutuels.
    followers = set(get_follower_screennames_by_user_id(db, user_id))
    followings = set(get_following_screennames_by_user_id(db, user_id))
    mutual_screennames = list(followers.intersection(followings))

    return mutual_screennames


def get_users_screennames_with_more_than_n_followers(db, n):
    """
    Retrieve the screen names of users who have more than 'n' followers.
    """
    followers_count_pipeline = [
        {"$group": {
            "_id": "$targetIdUser",
            "count": {"$sum": 1}
        }},
        {"$match": {
            "count": {"$gt": n}
        }},
        {"$lookup": {
            "from": "users",
            "localField": "_id",
            "foreignField": "idUser",  # Adjust to the correct field in 'users'
            "as": "user_data"
        }},
        {"$match": {
            "user_data": {"$ne": []}  # Ensures the lookup found a user
        }},
        {"$project": {
            "screenName": {"$arrayElemAt": ["$user_data.screenName", 0]}
        }}
    ]

    users_screennames = [
        doc['screenName'] for doc in db.get_collection('user_follows').aggregate(followers_count_pipeline)
    ]

    return users_screennames


def get_users_screennames_with_more_than_n_followings(db, n):
    """
    Retrieve the screen names of users who follow more than 'n' users.
    """
    followings_count_pipeline = [
        {"$group": {
            "_id": "$sourceIdUser",
            "count": {"$sum": 1}
        }},
        {"$match": {
            "count": {"$gt": n}
        }},
        {"$lookup": {
            "from": "users",
            "localField": "_id",
            "foreignField": "idUser",  # Adjust to the correct field in 'users'
            "as": "user_data"
        }},
        {"$match": {
            "user_data": {"$ne": []}  # Ensures the lookup found a user
        }},
        {"$project": {
            "screenName": {"$arrayElemAt": ["$user_data.screenName", 0]}
        }}
    ]

    users_screennames = [
        doc['screenName'] for doc in db.get_collection('user_follows').aggregate(followings_count_pipeline)
    ]

    return users_screennames
