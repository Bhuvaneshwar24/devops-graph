from app.database import driver


def test_incident_impact(session):
    query = """
    MATCH (i:Incident {id: $incident_id})
          -[:AFFECTED]->(affected:Service)
    OPTIONAL MATCH
          (affected)-[:DEPENDS_ON*1..3]->(downstream:Service)
    RETURN DISTINCT
        i.id AS incident_id,
        i.title AS incident,
        affected.name AS affected_service,
        downstream.name AS downstream_service
    ORDER BY downstream_service
    """

    result = session.run(
        query,
        incident_id="INC-102",
    )

    print("\n=== INCIDENT IMPACT ===")

    for record in result:
        print(
            f"{record['incident_id']} | "
            f"{record['affected_service']} -> "
            f"{record['downstream_service']}"
        )


def test_database_blast_radius(session):
    query = """
    MATCH (db:Database {id: $database_id})
          <-[:USES_DATABASE]-(direct:Service)
    OPTIONAL MATCH
          (dependent:Service)-[:DEPENDS_ON*1..3]->(direct)
    RETURN DISTINCT
        db.name AS database,
        direct.name AS direct_service,
        dependent.name AS dependent_service
    ORDER BY direct_service, dependent_service
    """

    result = session.run(
        query,
        database_id="db-orders",
    )

    print("\n=== DATABASE BLAST RADIUS ===")

    for record in result:
        print(
            f"{record['database']} | "
            f"Direct: {record['direct_service']} | "
            f"Dependent: {record['dependent_service']}"
        )


def test_deployment_impact(session):
    query = """
    MATCH (deployment:Deployment {id: $deployment_id})
          -[:DEPLOYED]->(service:Service)
    OPTIONAL MATCH
          (service)-[:DEPENDS_ON*1..3]->(dependent:Service)
    OPTIONAL MATCH
          (incident:Incident)-[:CAUSED_BY]->(deployment)
    RETURN DISTINCT
        deployment.id AS deployment_id,
        deployment.version AS version,
        service.name AS deployed_service,
        dependent.name AS dependent_service,
        collect(DISTINCT incident.id) AS incidents
    ORDER BY dependent_service
    """

    result = session.run(
        query,
        deployment_id="DEP-004",
    )

    print("\n=== DEPLOYMENT IMPACT ===")

    for record in result:
        print(
            f"{record['deployment_id']} | "
            f"{record['version']} | "
            f"Service: {record['deployed_service']} | "
            f"Dependent: {record['dependent_service']} | "
            f"Incidents: {record['incidents']}"
        )


try:
    with driver.session() as session:
        test_incident_impact(session)
        test_database_blast_radius(session)
        test_deployment_impact(session)

    print("\nAll query tests completed successfully.")

finally:
    driver.close()