from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.api.deps import CurrentUser, DbSession
from app.models import Service
from app.schemas.service import ServiceCreate, ServiceRead, ServiceUpdate

router = APIRouter(prefix="/services", tags=["services"])


def _get_or_404(db: DbSession, service_id: int) -> Service:
    service = db.get(Service, service_id)
    if service is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Service not found")
    return service


def _commit_or_conflict(db: DbSession) -> None:
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "Slug already in use") from None


@router.get("", response_model=list[ServiceRead])
def list_services(
    db: DbSession,
    include_inactive: bool = False,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
) -> list[Service]:
    stmt = select(Service).order_by(Service.name).offset(skip).limit(limit)
    if not include_inactive:
        stmt = stmt.where(Service.is_active.is_(True))
    return list(db.scalars(stmt))


@router.get("/{service_id}", response_model=ServiceRead)
def get_service(service_id: int, db: DbSession) -> Service:
    return _get_or_404(db, service_id)


@router.post("", response_model=ServiceRead, status_code=status.HTTP_201_CREATED)
def create_service(payload: ServiceCreate, db: DbSession, _: CurrentUser) -> Service:
    service = Service(**payload.model_dump())
    db.add(service)
    _commit_or_conflict(db)
    db.refresh(service)
    return service


@router.patch("/{service_id}", response_model=ServiceRead)
def update_service(
    service_id: int, payload: ServiceUpdate, db: DbSession, _: CurrentUser
) -> Service:
    service = _get_or_404(db, service_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(service, field, value)
    _commit_or_conflict(db)
    db.refresh(service)
    return service


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(service_id: int, db: DbSession, _: CurrentUser) -> None:
    db.delete(_get_or_404(db, service_id))
    db.commit()
