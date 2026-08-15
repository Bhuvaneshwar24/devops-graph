from app.database import driver


QUERY = """
MATCH (i:Incident {id: $incident_id})
      -[:AFFECTED]->(affected:Service)
      -[:DEPENDS_ON*1..3]->(downstream:Service)
RETURN DISTINCT
    i.id AS incident,
    affected.name AS affected_service,
    downstream.name AS downstream_service
ORDER BY affected_service, downstream_service
"""

try:
    with driver.session() as session:
        result = session.run(
            QUERY,
            incident_id="INC-102",
        )

        print("Multi-hop incident impact analysis:")
        print("-" * 60)

        found = False

        for record in result:
            found = True
            print(
                f"Incident: {record['incident']}"
                f" | Affected: {record['affected_service']}"
                f" | Downstream: {record['downstream_service']}"
            )

        if not found:
            print("No downstream services found.")

finally:
    driver.close()