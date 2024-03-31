from neo4j import GraphDatabase


class Neo4J:
    def __init__(self):
        # Établissement de la connexion au driver Neo4j. Remplacer les identifiants par les vôtres.
        self._driver = GraphDatabase.driver('neo4j+s://6c66aa85.databases.neo4j.io',
                                            auth=('neo4j', 'ACu8O0LLEs6te3lkqLI2XG_o0tQnZs7_w7nWflQaxbs'))

    def close(self):
        """Close the Neo4j driver."""
        # Ferme la connexion au driver Neo4j.
        self._driver.close()

    def query(self, query, params=None):
        """Execute a query against the Neo4j database."""
        # Exécute une requête sur la base de données Neo4j et retourne les résultats.
        with self._driver.session() as session:
            result = session.run(query, parameters=params or {})
            return [record for record in result]

    # Create a node:
    def create_node(self, label, properties):
        """Create a node in the Neo4j database."""
        # Crée un noeud dans la base de données Neo4j.
        query = f"CREATE (n:{label} $properties)"
        self.query(query, params={"properties": properties})

    # Create a relationship:
    def create_relationship(self, label1, label2, properties):
        """Create a relationship between two nodes in the Neo4j database."""
        # Crée une relation entre deux noeuds dans la base de données Neo4j.
        query = f"""
            MATCH (a:{label1}), (b:{label2})
            WHERE a.id = $id1 AND b.id = $id2
            CREATE (a)-[:RELATIONSHIP $properties]->(b)
            """
        self.query(query, params=properties)