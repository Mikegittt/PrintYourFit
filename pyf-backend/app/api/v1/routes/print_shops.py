from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.v1.deps import get_db, get_current_active_user, require_role
from app.models.print_shop import PrintShop
from app.schemas.user import UserResponse

router = APIRouter()

@router.post("/register", response_model=dict)
async def register_shop(payload: dict, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_active_user)):
    if current_user.role != "PRINT_SHOP":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only print shop users can register shops")
    shop = PrintShop(
        user_id=current_user.id,
        shop_name=payload.get("shop_name"),
        address=payload.get("address"),
        state=payload.get("state"),
        status="PENDING",
    )
    db.add(shop)
    await db.commit()
    await db.refresh(shop)
    return {"shop_id": str(shop.id), "status": "PENDING"}

@router.get("/", response_model=list[dict], dependencies=[Depends(require_role("ADMIN"))])
async def list_print_shops(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PrintShop))
    shops = result.scalars().all()
    return [{"id": str(s.id), "shop_name": s.shop_name, "status": s.status, "created_at": str(s.created_at)} for s in shops]


@router.get("/discover", response_model=list[dict])
async def discover_print_shops(q: str | None = None, db: AsyncSession = Depends(get_db)):
    # Public discovery endpoint: only APPROVED shops are returned
    stmt = select(PrintShop).where(PrintShop.status == "APPROVED")
    result = await db.execute(stmt)
    shops = result.scalars().all()
    items = []
    for s in shops:
        if q:
            if q.lower() in (s.shop_name or "").lower() or q.lower() in (s.address or "").lower():
                items.append({"id": str(s.id), "shop_name": s.shop_name, "address": s.address, "state": s.state})
        else:
            items.append({"id": str(s.id), "shop_name": s.shop_name, "address": s.address, "state": s.state})
    return items

@router.get("/pending", response_model=list[dict], dependencies=[Depends(require_role("ADMIN"))])
async def list_pending_shops(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PrintShop).where(PrintShop.status == "PENDING"))
    shops = result.scalars().all()
    return [{"id": str(s.id), "shop_name": s.shop_name, "address": s.address, "state": s.state, "status": s.status, "created_at": str(s.created_at)} for s in shops]

@router.get("/{shop_id}", response_model=dict)
async def get_print_shop(shop_id: str, db: AsyncSession = Depends(get_db)):
    shop = await db.get(PrintShop, shop_id)
    if not shop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Print shop not found")
    return {"id": str(shop.id), "shop_name": shop.shop_name, "address": shop.address, "state": shop.state, "status": shop.status, "is_verified": shop.is_verified}

@router.put("/{shop_id}/approve", response_model=dict, dependencies=[Depends(require_role("ADMIN"))])
async def approve_shop(shop_id: str, db: AsyncSession = Depends(get_db)):
    shop = await db.get(PrintShop, shop_id)
    if not shop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Print shop not found")
    shop.status = "APPROVED"
    shop.is_verified = True
    db.add(shop)
    await db.commit()
    await db.refresh(shop)
    return {"id": str(shop.id), "status": "APPROVED"}

@router.put("/{shop_id}/reject", response_model=dict, dependencies=[Depends(require_role("ADMIN"))])
async def reject_shop(shop_id: str, db: AsyncSession = Depends(get_db)):
    shop = await db.get(PrintShop, shop_id)
    if not shop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Print shop not found")
    shop.status = "REJECTED"
    db.add(shop)
    await db.commit()
    await db.refresh(shop)
    return {"id": str(shop.id), "status": "REJECTED"}

@router.put("/{shop_id}/verify", response_model=dict, dependencies=[Depends(require_role("ADMIN"))])
async def verify_shop(shop_id: str, db: AsyncSession = Depends(get_db)):
    shop = await db.get(PrintShop, shop_id)
    if not shop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Print shop not found")
    shop.is_verified = True
    db.add(shop)
    await db.commit()
    await db.refresh(shop)
    return {"verified": True}
