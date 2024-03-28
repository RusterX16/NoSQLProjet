from pymongo import MongoClient


class MongoDB:
    databaseName = 'NoSQL'

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')

    def get_db(self):
        return self.client[self.databaseName]

    def get_collection(self, collection_name):
        return self.get_db()[collection_name]

    def get(self, collection_name, query, initial_match=None):
        return self.get_collection(collection_name).find(query, initial_match)

    def insert(self, collection_name, data):
        return self.get_collection(collection_name).insert_one(data)

    def update(self, collection_name, query, data):
        return self.get_collection(collection_name).update_one(query, data)

    def delete(self, collection_name, query):
        return self.get_collection(collection_name).delete_one(query)

    def count(self, collection_name, query=None):
        return self.get_collection(collection_name).count_documents(query)

    def aggregate(self, collection_name, pipeline):
        return self.get_collection(collection_name).aggregate(pipeline)

    def aggregate_join(self, from_collection, local_field, foreign_collection, foreign_field, as_field,
                       initial_match=None):
        pipeline = [
            {"$lookup": {
                "from": foreign_collection,
                "localField": local_field,
                "foreignField": foreign_field,
                "as": as_field
            }}
        ]
        if initial_match:
            pipeline.insert(0, {"$match": initial_match})
        return self.aggregate(from_collection, pipeline)

    def close(self):
        return self.client.close()
