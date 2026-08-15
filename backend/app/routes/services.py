from fastapi import APIRouter, HTTPException

from app.services.graph_service import (
    get_service,
    get_service_dependencies,
    get_services,
)


router = APIRouter(
    prefix="/api/services",
    tags=["Services"],
)


@router.get("")
def list_services():
    return {
        "data": get_services()
    }


@router.get("/{service_id}")
def service_details(service_id: str):
    service = get_service(service_id)

    if service is None:
        raise HTTPException(
            status_code=404,
            detail=f"Service '{service_id}' not found",
        )

    return {
        "data": service
    }


@router.get("/{service_id}/dependencies")
def service_dependencies(service_id: str):
    service = get_service(service_id)

    if service is None:
        raise HTTPException(
            status_code=404,
            detail=f"Service '{service_id}' not found",
        )

    return {
        "data": get_service_dependencies(service_id)
    }