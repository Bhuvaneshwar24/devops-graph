from app.database import driver


QUERY = """
MATCH (db:Database {id: $database_id})
      <-[:USES_DATABASE]-(service:Service)

OPTIONAL MATCH path =
      (dependent:Service)
      -[:DEPENDS_ON*1..3]->
      (service)

RETURN DISTINCT
    db.name AS database,
    service.name AS direct_service,
    dependent.name AS dependent_service,
    [node IN nodes(path) | node.name] AS dependency_path
ORDER BY direct_service, dependent_service
"""


try:
    with driver.session() as session:
        result = session.run(
            QUERY,
            database_id="db-orders",
        )

        print("Database dependency paths:")
        print("-" * 80)

        for record in result:
            print(
                f"Database: {record['database']}"
                f" | Direct service: {record['direct_service']}"
                f" | Dependent: {record['dependent_service']}"
                f" | Path: {' -> '.join(record['dependency_path'])}"
            )

finally:
    driver.close()