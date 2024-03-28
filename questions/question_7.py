# ################################################################# #
# Question 7:                                                       #
# Donner le nom des followers de Spinomade (dans ce jeu de données) #
# ################################################################# #
from db.mongodb_user_service import get_follower_screennames_by_user_id
from db.mongdb import MongoDB

db = MongoDB()
spinomade_user_doc = db.get_collection('users').find_one({"screenName": "Spinomade"})
if spinomade_user_doc:
    spinomade_id = spinomade_user_doc["idUser"]
    # Get the follower screen names using the user ID
    result = get_follower_screennames_by_user_id(db=db, user_id=spinomade_id)
    follower_count = len(result)
    print(f"Followers de Spinomade ({follower_count}): {result}")
else:
    print("User not found.")
