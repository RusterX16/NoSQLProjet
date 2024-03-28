# ##################################################################################### #
# Question 9:                                                                           #
# Donner le nom des utilisateurs qui sont à la fois followers et followees de Spinomade #
# ##################################################################################### #
from db.mongodb_user_service import get_mutual_screennames_by_user_id
from db.mongdb import MongoDB

db = MongoDB()
spinomade_user_doc = db.get_collection('users').find_one({"screenName": "Spinomade"})
if spinomade_user_doc:
    spinomade_id = spinomade_user_doc["idUser"]
    # Get the mutual screen names using the user ID
    result = get_mutual_screennames_by_user_id(db=db, user_id=spinomade_id)
    mutual_count = len(result)
    print(f"Utilisateurs mutuels de Spinomade ({mutual_count}): {result}")
