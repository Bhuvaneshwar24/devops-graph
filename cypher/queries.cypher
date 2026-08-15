// ============================================================
// AI DevOps Incident Graph — Reusable Cypher Queries
// ============================================================


// 1. LIST ALL SERVICES
// Parameter: none

MATCH (s:Service)
RETURN
    s.id AS id,
    s.name AS name,
    s.description AS description,
    s.criticality AS criticality,
    s.status AS status
ORDER BY s.name;


// 2. GET A SINGLE SERVICE
// Parameter: $service_id

MATCH (s:Service {id: $service_id})
RETURN
    s.id AS id,
    s.name AS name,
    s.description AS description,
    s.criticality AS criticality,
    s.status AS status;


// 3. DIRECT SERVICE DEPENDENCIES
// Parameter: $service_id

MATCH (s:Service {id: $service_id})
OPTIONAL MATCH (s)-[r:DEPENDS_ON]->(dependency:Service)
RETURN
    s.name AS service,
    dependency.name AS dependency,
    r.criticality AS dependency_criticality
ORDER BY dependency.name;


// 4. MULTI-HOP SERVICE DEPENDENCIES
// Parameter: $service_id

MATCH (s:Service {id: $service_id})
      -[:DEPENDS_ON*1..3]->
      (dependency:Service)
RETURN DISTINCT
    s.name AS service,
    dependency.name AS dependency
ORDER BY dependency.name;


// 5. INCIDENT IMPACT / MULTI-HOP BLAST RADIUS
// Parameter: $incident_id

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
ORDER BY downstream_service;


// 6. INCIDENT INVESTIGATION
// Parameter: $incident_id

MATCH (i:Incident {id: $incident_id})
OPTIONAL MATCH (i)-[:AFFECTED]->(service:Service)
OPTIONAL MATCH (i)-[:TRIGGERED_BY]->(alert:Alert)
OPTIONAL MATCH (i)-[:CAUSED_BY]->(deployment:Deployment)
OPTIONAL MATCH (i)-[:RESOLVED_BY]->(resolver:Engineer)
OPTIONAL MATCH (i)-[:HAS_RUNBOOK]->(runbook:Runbook)
RETURN
    i.id AS incident_id,
    i.title AS title,
    i.severity AS severity,
    i.status AS status,
    i.started_at AS started_at,
    i.resolved_at AS resolved_at,
    collect(DISTINCT service.name) AS affected_services,
    collect(DISTINCT alert.name) AS alerts,
    collect(DISTINCT deployment.version) AS deployments,
    collect(DISTINCT resolver.name) AS resolvers,
    collect(DISTINCT runbook.title) AS runbooks;


// 7. DATABASE BLAST RADIUS
// Parameter: $database_id

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
    dependent_service;


// 8. DATABASE DEPENDENCY PATHS
// Parameter: $database_id

MATCH (db:Database {id: $database_id})
      <-[:USES_DATABASE]-
      (direct:Service)
OPTIONAL MATCH path =
      (dependent:Service)
      -[:DEPENDS_ON*1..3]->
      (direct)
RETURN DISTINCT
    db.name AS database,
    direct.name AS direct_service,
    dependent.name AS dependent_service,
    [node IN nodes(path) | node.name] AS dependency_path
ORDER BY
    direct_service,
    dependent_service;


// 9. DEPLOYMENT IMPACT
// Parameter: $deployment_id

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
ORDER BY dependent_service;


// 10. SERVICE OWNERSHIP
// Parameter: $service_id

MATCH (team:Team)-[:OWNS]->(service:Service {id: $service_id})
OPTIONAL MATCH (engineer:Engineer)-[:MEMBER_OF]->(team)
RETURN
    service.name AS service,
    team.name AS owning_team,
    collect(DISTINCT engineer.name) AS team_members;


// 11. INCIDENT RESPONDERS
// Parameter: $incident_id

MATCH (engineer:Engineer)-[:RESPONDED_TO]->(incident:Incident {id: $incident_id})
RETURN
    incident.id AS incident_id,
    incident.title AS incident,
    engineer.id AS engineer_id,
    engineer.name AS engineer,
    engineer.role AS role
ORDER BY engineer.name;


// 12. SERVICES USING A DATABASE
// Parameter: $database_id

MATCH (service:Service)-[:USES_DATABASE]->(db:Database {id: $database_id})
RETURN
    db.name AS database,
    service.id AS service_id,
    service.name AS service,
    service.criticality AS criticality
ORDER BY service.name;


// 13. SEARCH SERVICES, INCIDENTS, AND DEPLOYMENTS
// Parameter: $search_term

MATCH (node)
WHERE
    (node:Service OR node:Incident OR node:Deployment)
    AND (
        toLower(coalesce(node.name, "")) CONTAINS toLower($search_term)
        OR toLower(coalesce(node.title, "")) CONTAINS toLower($search_term)
        OR toLower(coalesce(node.version, "")) CONTAINS toLower($search_term)
        OR toLower(coalesce(node.id, "")) CONTAINS toLower($search_term)
    )
RETURN
    labels(node) AS labels,
    node.id AS id,
    coalesce(node.name, node.title, node.version) AS name
ORDER BY name;


// 14. CRITICAL INCIDENTS
// Parameter: $severity

MATCH (i:Incident {severity: $severity})
OPTIONAL MATCH (i)-[:AFFECTED]->(service:Service)
RETURN
    i.id AS incident_id,
    i.title AS title,
    i.severity AS severity,
    i.status AS status,
    collect(DISTINCT service.name) AS affected_services
ORDER BY i.started_at DESC;