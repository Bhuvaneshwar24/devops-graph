from fastapi import APIRouter, Query

from app.services.graph_service import search_graph


router = APIRouter(
    prefix="/api",
    tags=["Search"],
)


@router.get("/search")
def search(
    q: str = Query(
        ...,
        min_length=1,
        description="Search services, incidents, and deployments",
    )
):
    return {
        "query": q,
        "data": search_graph(q),
    }