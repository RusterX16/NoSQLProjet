from neo4j import GraphDatabase


class Neo4J:
    def __init__(self):
        self._driver = GraphDatabase.driver('neo4j+s://6c66aa85.databases.neo4j.io',
                                            auth=('neo4j', 'ACu8O0LLEs6te3lkqLI2XG_o0tQnZs7_w7nWflQaxbs'))

    def close(self):
        self._driver.close()

    def query(self, query, params=None):
        with self._driver.session() as session:
            result = session.run(query, parameters=params or {})
            return [record for record in result]
