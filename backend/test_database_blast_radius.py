from app.database import driver


QUERY = """
MATCH (db:Database {id: $database_id})
      <-[:USES_DATABASE]-(service:Service)
OPTIONAL MATCH (dependent:Service)
      -[:DEPENDS_ON*1..3]->(service)
RETURN DISTINCT
    db.name AS database,
    service.name AS directly_using_service,
    dependent.name AS dependent_service
ORDER BY directly_using_service, dependent_service
"""


try:
    with driver.session() as session:
        result = session.run(
            QUERY,
            database_id="db-orders",
        )

        print("Database blast-radius analysis:")
        print("-" * 70)

        found = False

        for record in result:
            found = True

            dependent = record["dependent_service"]

            if dependent:
                print(
                    f"Database: {record['database']}"
                    f" | Direct service: {record['directly_using_service']}"
                    f" | Dependent service: {dependent}"
                )
            else:
                print(
                    f"Database: {record['database']}"
                    f" | Direct service: {record['directly_using_service']}"
                    f" | Dependent service: None"
                )

        if not found:
            print("No services found.")

finally:
    driver.close()