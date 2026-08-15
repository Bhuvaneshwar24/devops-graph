from fastapi import APIRouter, HTTPException

from app.services.graph_service import (
    get_database_blast_radius,
    get_databases,
    get_deployment_impact,
    get_deployments,
    get_incident_impact,
    get_incidents,
)


router = APIRouter(
    prefix="/api",
    tags=["Graph Analysis"],
)


@router.get("/incidents")
def list_incidents():
    return {
        "data": get_incidents()
    }


@router.get("/incidents/{incident_id}/impact")
def incident_impact(incident_id: str):
    data = get_incident_impact(incident_id)

    if not data:
        raise HTTPException(
            status_code=404,
            detail=f"Incident '{incident_id}' not found",
        )

    return {
        "data": data
    }


@router.get("/databases")
def list_databases():
    return {
        "data": get_databases()
    }


@router.get("/databases/{database_id}/blast-radius")
def database_blast_radius(database_id: str):
    data = get_database_blast_radius(database_id)

    if not data:
        raise HTTPException(
            status_code=404,
            detail=f"Database '{database_id}' not found",
        )

    return {
        "data": data
    }


@router.get("/deployments")
def list_deployments():
    return {
        "data": get_deployments()
    }


@router.get("/deployments/{deployment_id}/impact")
def deployment_impact(deployment_id: str):
    data = get_deployment_impact(deployment_id)

    if not data:
        raise HTTPException(
            status_code=404,
            detail=f"Deployment '{deployment_id}' not found",
        )

    return {
        "data": data
    }