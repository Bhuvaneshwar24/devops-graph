"""
Graph service layer.

Contains reusable CognoDB queries used by the FastAPI routes.
"""

from typing import Any

from app.database import driver


def get_services() -> list[dict[str, Any]]:
    query = """
    MATCH (s:Service)
    RETURN
        s.id AS id,
        s.name AS name,
        s.description AS description,
        s.criticality AS criticality,
        s.status AS status
    ORDER BY s.name
    """

    with driver.session() as session:
        result = session.run(query)

        return [record.data() for record in result]


def get_service(service_id: str) -> dict[str, Any] | None:
    query = """
    MATCH (s:Service {id: $service_id})
    RETURN
        s.id AS id,
        s.name AS name,
        s.description AS description,
        s.criticality AS criticality,
        s.status AS status
    """

    with driver.session() as session:
        record = session.run(
            query,
            service_id=service_id,
        ).single()

        return record.data() if record else None


def get_service_dependencies(
    service_id: str,
) -> list[dict[str, Any]]:
    query = """
    MATCH (s:Service {id: $service_id})
    OPTIONAL MATCH (s)-[r:DEPENDS_ON]->(dependency:Service)
    RETURN
        s.name AS service,
        dependency.name AS dependency,
        r.criticality AS dependency_criticality
    ORDER BY dependency.name
    """

    with driver.session() as session:
        result = session.run(
            query,
            service_id=service_id,
        )

        return [record.data() for record in result]


def get_incidents() -> list[dict[str, Any]]:
    query = """
    MATCH (i:Incident)
    RETURN
        i.id AS id,
        i.title AS title,
        i.severity AS severity,
        i.status AS status
    ORDER BY i.title
    """

    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]


def get_databases() -> list[dict[str, Any]]:
    query = """
    MATCH (db:Database)
    RETURN
        db.id AS id,
        db.name AS name,
        db.engine AS engine
    ORDER BY db.name
    """

    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]


def get_deployments() -> list[dict[str, Any]]:
    query = """
    MATCH (d:Deployment)
    RETURN
        d.id AS id,
        d.version AS version,
        d.status AS status,
        d.deployed_at AS deployed_at
    ORDER BY d.version
    """

    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]


def get_incident_impact(
    incident_id: str,
) -> list[dict[str, Any]]:
    query = """
    MATCH (i:Incident {id: $incident_id})
          -[:AFFECTED]->
          (affected:Service)

    OPTIONAL MATCH
          (affected)-[:DEPENDS_ON*1..3]->
          (downstream:Service)

    RETURN DISTINCT
        i.id AS incident_id,
        i.title AS incident,
        affected.name AS affected_service,
        downstream.name AS downstream_service

    ORDER BY downstream_service
    """

    with driver.session() as session:
        result = session.run(
            query,
            incident_id=incident_id,
        )

        return [record.data() for record in result]


def get_database_blast_radius(
    database_id: str,
) -> list[dict[str, Any]]:
    query = """
    MATCH (db:Database {id: $database_id})
          <-[:USES_DATABASE]-
          (direct:Service)

    OPTIONAL MATCH
          (dependent:Service)
          -[:DEPENDS_ON*1..3]->
          (direct)

    RETURN DISTINCT
        db.id AS database_id,
        db.name AS database,
        direct.name AS directly_affected_service,
        dependent.name AS dependent_service

    ORDER BY
        directly_affected_service,
        dependent_service
    """

    with driver.session() as session:
        result = session.run(
            query,
            database_id=database_id,
        )

        return [record.data() for record in result]


def get_deployment_impact(
    deployment_id: str,
) -> list[dict[str, Any]]:
    query = """
    MATCH (deployment:Deployment {id: $deployment_id})
          -[:DEPLOYED]->
          (service:Service)

    OPTIONAL MATCH
          (service)-[:DEPENDS_ON*1..3]->
          (dependent:Service)

    OPTIONAL MATCH
          (incident:Incident)-[:CAUSED_BY]->
          (deployment)

    RETURN DISTINCT
        deployment.id AS deployment_id,
        deployment.version AS version,
        deployment.status AS deployment_status,
        service.name AS deployed_service,
        dependent.name AS dependent_service,
        collect(DISTINCT incident.id) AS related_incidents

    ORDER BY dependent_service
    """

    with driver.session() as session:
        result = session.run(
            query,
            deployment_id=deployment_id,
        )

        return [record.data() for record in result]


def search_graph(search_term: str) -> list[dict[str, Any]]:
    query = """
    MATCH (node)
    WHERE
        (node:Service OR node:Incident OR node:Database OR node:Deployment)
        AND (
            toLower(coalesce(node.name, "")) CONTAINS
                toLower($search_term)
            OR toLower(coalesce(node.title, "")) CONTAINS
                toLower($search_term)
            OR toLower(coalesce(node.version, "")) CONTAINS
                toLower($search_term)
            OR toLower(coalesce(node.id, "")) CONTAINS
                toLower($search_term)
        )

    RETURN
        labels(node) AS labels,
        node.id AS id,
        coalesce(node.name, node.title, node.version) AS name

    ORDER BY name
    """

    with driver.session() as session:
        result = session.run(
            query,
            search_term=search_term,
        )

        return [record.data() for record in result]