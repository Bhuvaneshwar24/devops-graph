"""
Seed realistic DevOps incident data into CognoDB.

The script is intentionally idempotent:
- Nodes use MERGE with their unique IDs.
- Relationships use MERGE.
- Running the script multiple times does not create duplicates.
"""

from app.database import driver


SERVICES = [
    {
        "id": "svc-gateway",
        "name": "API Gateway",
        "description": "Entry point for client API traffic.",
        "criticality": "critical",
        "status": "healthy",
    },
    {
        "id": "svc-auth",
        "name": "Auth Service",
        "description": "Handles authentication and token validation.",
        "criticality": "critical",
        "status": "healthy",
    },
    {
        "id": "svc-checkout",
        "name": "Checkout API",
        "description": "Handles customer checkout workflows.",
        "criticality": "critical",
        "status": "degraded",
    },
    {
        "id": "svc-payment",
        "name": "Payment Service",
        "description": "Processes payment authorization and capture.",
        "criticality": "critical",
        "status": "healthy",
    },
    {
        "id": "svc-order",
        "name": "Order Service",
        "description": "Creates and manages customer orders.",
        "criticality": "high",
        "status": "healthy",
    },
    {
        "id": "svc-inventory",
        "name": "Inventory Service",
        "description": "Tracks product inventory and stock availability.",
        "criticality": "high",
        "status": "healthy",
    },
    {
        "id": "svc-notification",
        "name": "Notification Service",
        "description": "Sends email, SMS, and push notifications.",
        "criticality": "medium",
        "status": "healthy",
    },
    {
        "id": "svc-user",
        "name": "User Service",
        "description": "Manages customer profiles and preferences.",
        "criticality": "high",
        "status": "healthy",
    },
    {
        "id": "svc-shipping",
        "name": "Shipping Service",
        "description": "Handles shipment creation and delivery tracking.",
        "criticality": "high",
        "status": "healthy",
    },
    {
        "id": "svc-recommendation",
        "name": "Recommendation Service",
        "description": "Generates personalized product recommendations.",
        "criticality": "low",
        "status": "healthy",
    },
]


TEAMS = [
    {
        "id": "team-platform",
        "name": "Platform Engineering",
    },
    {
        "id": "team-commerce",
        "name": "Commerce Engineering",
    },
    {
        "id": "team-payments",
        "name": "Payments Engineering",
    },
    {
        "id": "team-customer",
        "name": "Customer Experience Engineering",
    },
]


ENGINEERS = [
    {
        "id": "eng-001",
        "name": "Arjun Mehta",
        "role": "Senior Platform Engineer",
    },
    {
        "id": "eng-002",
        "name": "Priya Nair",
        "role": "Site Reliability Engineer",
    },
    {
        "id": "eng-003",
        "name": "Rahul Sharma",
        "role": "Senior Backend Engineer",
    },
    {
        "id": "eng-004",
        "name": "Ananya Rao",
        "role": "Backend Engineer",
    },
    {
        "id": "eng-005",
        "name": "Vikram Patel",
        "role": "Payments Engineer",
    },
    {
        "id": "eng-006",
        "name": "Neha Iyer",
        "role": "Frontend Platform Engineer",
    },
    {
        "id": "eng-007",
        "name": "Karan Singh",
        "role": "SRE",
    },
    {
        "id": "eng-008",
        "name": "Meera Joshi",
        "role": "Customer Experience Engineer",
    },
]


ENVIRONMENTS = [
    {
        "id": "env-production",
        "name": "production",
    },
    {
        "id": "env-staging",
        "name": "staging",
    },
    {
        "id": "env-dev",
        "name": "dev",
    },
]


DATABASES = [
    {
        "id": "db-orders",
        "name": "Orders PostgreSQL",
        "engine": "PostgreSQL",
    },
    {
        "id": "db-payments",
        "name": "Payments PostgreSQL",
        "engine": "PostgreSQL",
    },
    {
        "id": "db-inventory",
        "name": "Inventory PostgreSQL",
        "engine": "PostgreSQL",
    },
    {
        "id": "db-users",
        "name": "Users PostgreSQL",
        "engine": "PostgreSQL",
    },
]


ALERTS = [
    {
        "id": "alert-001",
        "name": "Payment Latency High",
        "metric": "payment_api_latency_ms",
        "threshold": 1000,
        "fired_at": "2026-08-10T09:42:00Z",
    },
    {
        "id": "alert-002",
        "name": "Checkout Error Rate High",
        "metric": "checkout_error_rate",
        "threshold": 5,
        "fired_at": "2026-08-09T14:18:00Z",
    },
    {
        "id": "alert-003",
        "name": "Orders Database Connections",
        "metric": "orders_db_connections",
        "threshold": 90,
        "fired_at": "2026-08-08T11:20:00Z",
    },
    {
        "id": "alert-004",
        "name": "Inventory API Latency",
        "metric": "inventory_api_latency_ms",
        "threshold": 800,
        "fired_at": "2026-08-07T16:31:00Z",
    },
    {
        "id": "alert-005",
        "name": "Authentication Error Rate",
        "metric": "auth_error_rate",
        "threshold": 3,
        "fired_at": "2026-08-06T08:14:00Z",
    },
    {
        "id": "alert-006",
        "name": "Notification Queue Depth",
        "metric": "notification_queue_depth",
        "threshold": 5000,
        "fired_at": "2026-08-05T19:45:00Z",
    },
    {
        "id": "alert-007",
        "name": "Shipping API Errors",
        "metric": "shipping_error_rate",
        "threshold": 4,
        "fired_at": "2026-08-04T12:07:00Z",
    },
    {
        "id": "alert-008",
        "name": "User Database Connections",
        "metric": "users_db_connections",
        "threshold": 85,
        "fired_at": "2026-08-03T10:12:00Z",
    },
]


INCIDENTS = [
    {
        "id": "INC-101",
        "title": "Payment authorization latency spike",
        "severity": "sev1",
        "status": "resolved",
        "started_at": "2026-08-10T09:40:00Z",
        "resolved_at": "2026-08-10T10:25:00Z",
    },
    {
        "id": "INC-102",
        "title": "Checkout error rate increased",
        "severity": "sev2",
        "status": "resolved",
        "started_at": "2026-08-09T14:15:00Z",
        "resolved_at": "2026-08-09T15:05:00Z",
    },
    {
        "id": "INC-103",
        "title": "Orders database connection saturation",
        "severity": "sev2",
        "status": "resolved",
        "started_at": "2026-08-08T11:18:00Z",
        "resolved_at": "2026-08-08T12:10:00Z",
    },
    {
        "id": "INC-104",
        "title": "Inventory response degradation",
        "severity": "sev3",
        "status": "resolved",
        "started_at": "2026-08-07T16:28:00Z",
        "resolved_at": "2026-08-07T17:20:00Z",
    },
    {
        "id": "INC-105",
        "title": "Authentication failures in production",
        "severity": "sev2",
        "status": "resolved",
        "started_at": "2026-08-06T08:10:00Z",
        "resolved_at": "2026-08-06T08:55:00Z",
    },
    {
        "id": "INC-106",
        "title": "Notification backlog after deployment",
        "severity": "sev3",
        "status": "resolved",
        "started_at": "2026-08-05T19:40:00Z",
        "resolved_at": "2026-08-05T20:35:00Z",
    },
    {
        "id": "INC-107",
        "title": "Shipping provider API failures",
        "severity": "sev2",
        "status": "resolved",
        "started_at": "2026-08-04T12:05:00Z",
        "resolved_at": "2026-08-04T13:00:00Z",
    },
    {
        "id": "INC-108",
        "title": "User profile database saturation",
        "severity": "sev3",
        "status": "resolved",
        "started_at": "2026-08-03T10:10:00Z",
        "resolved_at": "2026-08-03T10:50:00Z",
    },
]


DEPLOYMENTS = [
    {
        "id": "DEP-001",
        "version": "gateway-3.4.1",
        "deployed_at": "2026-08-02T09:00:00Z",
        "status": "success",
    },
    {
        "id": "DEP-002",
        "version": "auth-5.2.0",
        "deployed_at": "2026-08-06T07:30:00Z",
        "status": "success",
    },
    {
        "id": "DEP-003",
        "version": "checkout-8.1.0",
        "deployed_at": "2026-08-09T13:45:00Z",
        "status": "success",
    },
    {
        "id": "DEP-004",
        "version": "payment-2.8.1",
        "deployed_at": "2026-08-10T09:15:00Z",
        "status": "rolled_back",
    },
    {
        "id": "DEP-005",
        "version": "order-6.7.2",
        "deployed_at": "2026-08-08T10:30:00Z",
        "status": "success",
    },
    {
        "id": "DEP-006",
        "version": "inventory-4.3.0",
        "deployed_at": "2026-08-07T15:50:00Z",
        "status": "success",
    },
    {
        "id": "DEP-007",
        "version": "notification-2.1.4",
        "deployed_at": "2026-08-05T19:10:00Z",
        "status": "failed",
    },
    {
        "id": "DEP-008",
        "version": "shipping-5.0.1",
        "deployed_at": "2026-08-04T11:30:00Z",
        "status": "success",
    },
    {
        "id": "DEP-009",
        "version": "user-7.2.0",
        "deployed_at": "2026-08-03T09:40:00Z",
        "status": "success",
    },
    {
        "id": "DEP-010",
        "version": "recommendation-1.9.3",
        "deployed_at": "2026-08-01T12:00:00Z",
        "status": "success",
    },
]


RUNBOOKS = [
    {
        "id": "RB-001",
        "title": "Payment Latency Investigation",
        "url": "https://example.com/runbooks/payment-latency",
    },
    {
        "id": "RB-002",
        "title": "Checkout Error Rate Investigation",
        "url": "https://example.com/runbooks/checkout-errors",
    },
    {
        "id": "RB-003",
        "title": "PostgreSQL Connection Saturation",
        "url": "https://example.com/runbooks/postgres-connections",
    },
    {
        "id": "RB-004",
        "title": "Authentication Failure Response",
        "url": "https://example.com/runbooks/auth-failures",
    },
    {
        "id": "RB-005",
        "title": "Notification Queue Recovery",
        "url": "https://example.com/runbooks/notification-queue",
    },
    {
        "id": "RB-006",
        "title": "External API Failure Response",
        "url": "https://example.com/runbooks/external-api",
    },
]


SERVICE_TEAM = [
    ("team-platform", "svc-gateway"),
    ("team-platform", "svc-auth"),
    ("team-commerce", "svc-checkout"),
    ("team-commerce", "svc-order"),
    ("team-commerce", "svc-inventory"),
    ("team-customer", "svc-notification"),
    ("team-customer", "svc-user"),
    ("team-customer", "svc-shipping"),
    ("team-customer", "svc-recommendation"),
    ("team-payments", "svc-payment"),
]


ENGINEER_TEAM = [
    ("eng-001", "team-platform"),
    ("eng-002", "team-platform"),
    ("eng-003", "team-commerce"),
    ("eng-004", "team-commerce"),
    ("eng-005", "team-payments"),
    ("eng-006", "team-customer"),
    ("eng-007", "team-platform"),
    ("eng-008", "team-customer"),
]


SERVICE_DATABASE = [
    ("svc-order", "db-orders"),
    ("svc-checkout", "db-orders"),
    ("svc-payment", "db-payments"),
    ("svc-inventory", "db-inventory"),
    ("svc-user", "db-users"),
]


SERVICE_DEPENDENCIES = [
    ("svc-gateway", "svc-auth", "hard"),
    ("svc-gateway", "svc-checkout", "hard"),
    ("svc-checkout", "svc-order", "hard"),
    ("svc-checkout", "svc-payment", "hard"),
    ("svc-order", "svc-inventory", "hard"),
    ("svc-order", "svc-payment", "hard"),
    ("svc-order", "svc-notification", "soft"),
    ("svc-shipping", "svc-order", "hard"),
    ("svc-recommendation", "svc-user", "soft"),
]


DEPLOYMENT_SERVICE = [
    ("DEP-001", "svc-gateway"),
    ("DEP-002", "svc-auth"),
    ("DEP-003", "svc-checkout"),
    ("DEP-004", "svc-payment"),
    ("DEP-005", "svc-order"),
    ("DEP-006", "svc-inventory"),
    ("DEP-007", "svc-notification"),
    ("DEP-008", "svc-shipping"),
    ("DEP-009", "svc-user"),
    ("DEP-010", "svc-recommendation"),
]


DEPLOYMENT_ENVIRONMENT = [
    ("DEP-001", "env-production"),
    ("DEP-002", "env-production"),
    ("DEP-003", "env-production"),
    ("DEP-004", "env-production"),
    ("DEP-005", "env-production"),
    ("DEP-006", "env-production"),
    ("DEP-007", "env-production"),
    ("DEP-008", "env-production"),
    ("DEP-009", "env-production"),
    ("DEP-010", "env-production"),
]


DEPLOYMENT_ENGINEER = [
    ("DEP-001", "eng-001"),
    ("DEP-002", "eng-002"),
    ("DEP-003", "eng-003"),
    ("DEP-004", "eng-005"),
    ("DEP-005", "eng-004"),
    ("DEP-006", "eng-004"),
    ("DEP-007", "eng-006"),
    ("DEP-008", "eng-008"),
    ("DEP-009", "eng-006"),
    ("DEP-010", "eng-008"),
]


INCIDENT_AFFECTED_SERVICE = [
    ("INC-101", "svc-payment"),
    ("INC-102", "svc-checkout"),
    ("INC-103", "svc-order"),
    ("INC-104", "svc-inventory"),
    ("INC-105", "svc-auth"),
    ("INC-106", "svc-notification"),
    ("INC-107", "svc-shipping"),
    ("INC-108", "svc-user"),
]


INCIDENT_ALERT = [
    ("INC-101", "alert-001"),
    ("INC-102", "alert-002"),
    ("INC-103", "alert-003"),
    ("INC-104", "alert-004"),
    ("INC-105", "alert-005"),
    ("INC-106", "alert-006"),
    ("INC-107", "alert-007"),
    ("INC-108", "alert-008"),
]


INCIDENT_DEPLOYMENT = [
    ("INC-101", "DEP-004"),
    ("INC-102", "DEP-003"),
    ("INC-103", "DEP-005"),
    ("INC-104", "DEP-006"),
    ("INC-105", "DEP-002"),
    ("INC-106", "DEP-007"),
    ("INC-107", "DEP-008"),
    ("INC-108", "DEP-009"),
]


INCIDENT_RESPONDER = [
    ("INC-101", "eng-005"),
    ("INC-101", "eng-002"),
    ("INC-102", "eng-003"),
    ("INC-103", "eng-004"),
    ("INC-103", "eng-002"),
    ("INC-104", "eng-004"),
    ("INC-105", "eng-002"),
    ("INC-106", "eng-006"),
    ("INC-107", "eng-008"),
    ("INC-108", "eng-006"),
]


INCIDENT_RESOLVER = [
    ("INC-101", "eng-005"),
    ("INC-102", "eng-003"),
    ("INC-103", "eng-002"),
    ("INC-104", "eng-004"),
    ("INC-105", "eng-002"),
    ("INC-106", "eng-006"),
    ("INC-107", "eng-008"),
    ("INC-108", "eng-006"),
]


INCIDENT_RUNBOOK = [
    ("INC-101", "RB-001"),
    ("INC-102", "RB-002"),
    ("INC-103", "RB-003"),
    ("INC-104", "RB-003"),
    ("INC-105", "RB-004"),
    ("INC-106", "RB-005"),
    ("INC-107", "RB-006"),
    ("INC-108", "RB-003"),
]


def seed_nodes(session) -> None:
    session.run(
        """
        UNWIND $services AS item
        MERGE (s:Service {id: item.id})
        SET s.name = item.name,
            s.description = item.description,
            s.criticality = item.criticality,
            s.status = item.status
        """,
        services=SERVICES,
    )

    session.run(
        """
        UNWIND $teams AS item
        MERGE (t:Team {id: item.id})
        SET t.name = item.name
        """,
        teams=TEAMS,
    )

    session.run(
        """
        UNWIND $engineers AS item
        MERGE (e:Engineer {id: item.id})
        SET e.name = item.name,
            e.role = item.role
        """,
        engineers=ENGINEERS,
    )

    session.run(
        """
        UNWIND $environments AS item
        MERGE (env:Environment {id: item.id})
        SET env.name = item.name
        """,
        environments=ENVIRONMENTS,
    )

    session.run(
        """
        UNWIND $databases AS item
        MERGE (db:Database {id: item.id})
        SET db.name = item.name,
            db.engine = item.engine
        """,
        databases=DATABASES,
    )

    session.run(
        """
        UNWIND $alerts AS item
        MERGE (a:Alert {id: item.id})
        SET a.name = item.name,
            a.metric = item.metric,
            a.threshold = item.threshold,
            a.fired_at = item.fired_at
        """,
        alerts=ALERTS,
    )

    session.run(
        """
        UNWIND $incidents AS item
        MERGE (i:Incident {id: item.id})
        SET i.title = item.title,
            i.severity = item.severity,
            i.status = item.status,
            i.started_at = item.started_at,
            i.resolved_at = item.resolved_at
        """,
        incidents=INCIDENTS,
    )

    session.run(
        """
        UNWIND $deployments AS item
        MERGE (d:Deployment {id: item.id})
        SET d.version = item.version,
            d.deployed_at = item.deployed_at,
            d.status = item.status
        """,
        deployments=DEPLOYMENTS,
    )

    session.run(
        """
        UNWIND $runbooks AS item
        MERGE (r:Runbook {id: item.id})
        SET r.title = item.title,
            r.url = item.url
        """,
        runbooks=RUNBOOKS,
    )


def seed_relationships(session) -> None:
    session.run(
        """
        UNWIND $items AS item
        MATCH (t:Team {id: item[0]})
        MATCH (s:Service {id: item[1]})
        MERGE (t)-[:OWNS]->(s)
        """,
        items=SERVICE_TEAM,
    )

    session.run(
        """
        UNWIND $items AS item
        MATCH (e:Engineer {id: item[0]})
        MATCH (t:Team {id: item[1]})
        MERGE (e)-[:MEMBER_OF]->(t)
        """,
        items=ENGINEER_TEAM,
    )

    session.run(
        """
        UNWIND $items AS item
        MATCH (s:Service {id: item[0]})
        MATCH (db:Database {id: item[1]})
        MERGE (s)-[:USES_DATABASE]->(db)
        """,
        items=SERVICE_DATABASE,
    )

    session.run(
        """
        UNWIND $items AS item
        MATCH (source:Service {id: item[0]})
        MATCH (target:Service {id: item[1]})
        MERGE (source)-[r:DEPENDS_ON]->(target)
        SET r.criticality = item[2]
        """,
        items=SERVICE_DEPENDENCIES,
    )

    session.run(
        """
        UNWIND $items AS item
        MATCH (d:Deployment {id: item[0]})
        MATCH (s:Service {id: item[1]})
        MERGE (d)-[:DEPLOYED]->(s)
        """,
        items=DEPLOYMENT_SERVICE,
    )

    session.run(
        """
        UNWIND $items AS item
        MATCH (d:Deployment {id: item[0]})
        MATCH (env:Environment {id: item[1]})
        MERGE (d)-[:DEPLOYED_TO]->(env)
        """,
        items=DEPLOYMENT_ENVIRONMENT,
    )

    session.run(
        """
        UNWIND $items AS item
        MATCH (d:Deployment {id: item[0]})
        MATCH (e:Engineer {id: item[1]})
        MERGE (d)-[:CREATED_BY]->(e)
        """,
        items=DEPLOYMENT_ENGINEER,
    )

    session.run(
        """
        UNWIND $items AS item
        MATCH (i:Incident {id: item[0]})
        MATCH (s:Service {id: item[1]})
        MERGE (i)-[:AFFECTED]->(s)
        """,
        items=INCIDENT_AFFECTED_SERVICE,
    )

    session.run(
        """
        UNWIND $items AS item
        MATCH (i:Incident {id: item[0]})
        MATCH (a:Alert {id: item[1]})
        MERGE (i)-[:TRIGGERED_BY]->(a)
        """,
        items=INCIDENT_ALERT,
    )

    session.run(
        """
        UNWIND $items AS item
        MATCH (i:Incident {id: item[0]})
        MATCH (d:Deployment {id: item[1]})
        MERGE (i)-[:CAUSED_BY]->(d)
        """,
        items=INCIDENT_DEPLOYMENT,
    )

    session.run(
        """
        UNWIND $items AS item
        MATCH (e:Engineer {id: item[1]})
        MATCH (i:Incident {id: item[0]})
        MERGE (e)-[:RESPONDED_TO]->(i)
        """,
        items=INCIDENT_RESPONDER,
    )

    session.run(
        """
        UNWIND $items AS item
        MATCH (i:Incident {id: item[0]})
        MATCH (e:Engineer {id: item[1]})
        MERGE (i)-[:RESOLVED_BY]->(e)
        """,
        items=INCIDENT_RESOLVER,
    )

    session.run(
        """
        UNWIND $items AS item
        MATCH (i:Incident {id: item[0]})
        MATCH (r:Runbook {id: item[1]})
        MERGE (i)-[:HAS_RUNBOOK]->(r)
        """,
        items=INCIDENT_RUNBOOK,
    )


def main() -> None:
    try:
        with driver.session() as session:
            seed_nodes(session)
            seed_relationships(session)

        print("Seed completed successfully.")
        print("Created/updated:")
        print(f"  Services: {len(SERVICES)}")
        print(f"  Teams: {len(TEAMS)}")
        print(f"  Engineers: {len(ENGINEERS)}")
        print(f"  Environments: {len(ENVIRONMENTS)}")
        print(f"  Databases: {len(DATABASES)}")
        print(f"  Alerts: {len(ALERTS)}")
        print(f"  Incidents: {len(INCIDENTS)}")
        print(f"  Deployments: {len(DEPLOYMENTS)}")
        print(f"  Runbooks: {len(RUNBOOKS)}")

    finally:
        driver.close()


if __name__ == "__main__":
    main()