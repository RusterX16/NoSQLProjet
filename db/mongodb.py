from pymongo import MongoClient


class MongoDB:
    database_name = 'NoSQL'

    def __init__(self):
        # Connexion au client MongoDB. Modifier l'URL si nécessaire.
        self.client = MongoClient('mongodb://localhost:27017/')

    def get_db(self):
        """Retrieve the database instance."""
        # Retourne une instance de la base de données.
        return self.client[self.database_name]

    def get_collection(self, collection_name):
        """Retrieve a collection from the database."""
        # Accède à une collection spécifique dans la base de données.
        return self.get_db()[collection_name]

    def get(self, collection_name, query, initial_match=None):
        """Retrieve documents from a collection based on a query."""
        # Récupère des documents basés sur une requête.
        return self.get_collection(collection_name).find(query, initial_match)

    def insert(self, collection_name, data):
        """Insert a document into a collection."""
        # Insère un document dans une collection spécifiée.
        return self.get_collection(collection_name).insert_one(data)

    def update(self, collection_name, query, data):
        """Update a document in a collection."""
        # Met à jour un document. Utilise $set pour spécifier les champs à mettre à jour.
        return self.get_collection(collection_name).update_one(query, {"$set": data})

    def delete(self, collection_name, query):
        """Delete a document from a collection."""
        # Supprime un document basé sur une requête.
        return self.get_collection(collection_name).delete_one(query)

    def count(self, collection_name, query=None):
        """Count documents in a collection that match a query."""
        # Compte les documents qui correspondent à une requête dans une collection.
        return self.get_collection(collection_name).count_documents(query or {})

    def aggregate(self, collection_name, pipeline):
        """Perform an aggregation operation on a collection."""
        # Effectue une opération d'agrégation sur une collection.
        return self.get_collection(collection_name).aggregate(pipeline)

    def aggregate_join(self, from_collection, local_field, foreign_collection, foreign_field, as_field,
                       initial_match=None):
        """Perform a join operation between collections using aggregation."""
        # Effectue une opération de jointure entre collections en utilisant l'agrégation.
        pipeline = [
            {"$lookup": {
                "from": foreign_collection,
                "localField": local_field,
                "foreignField": foreign_field,
                "as": as_field
            }}
        ]
        if initial_match:
            # Ajoute une étape de correspondance initiale si fournie.
            pipeline.insert(0, {"$match": initial_match})
        return self.aggregate(from_collection, pipeline)

    def close(self):
        """Close the MongoDB client."""
        # Ferme la connexion au client MongoDB.
        self.client.close()
