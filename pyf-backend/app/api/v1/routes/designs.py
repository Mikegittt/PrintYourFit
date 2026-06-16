from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.v1.deps import get_db, get_current_active_user
from app.models.design import Design
from app.models.order import Order
from app.schemas.design import DesignCreate, DesignResponse, DesignExport, SendToPrinter
from app.services.design_service import generate_image_from_prompt, convert_image_format
from uuid import UUID
import base64
from uuid import uuid4
from datetime import datetime

router = APIRouter()

@router.post("/generate", response_model=DesignResponse)
async def generate_design(payload: DesignCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_active_user)):
    """Generate an AI design from a text prompt."""
    # Generate image using Hugging Face (handle service/network failures)
    try:
        image_bytes = await generate_image_from_prompt(payload.prompt)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Image generation failed: {e}")

    if not image_bytes:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Image generation service unavailable")

    # Prepare response fields
    image_b64 = base64.b64encode(image_bytes).decode()
    created_at = datetime.utcnow()

    # If no DB session is available, skip persistence but still return image preview
    if db is None:
        # try to coerce user id to UUID, fallback to random UUID
        try:
            user_uuid = UUID(getattr(current_user, "id", None) or current_user.get("id") or current_user.get("sub"))
        except Exception:
            user_uuid = uuid4()

        return {
            "id": uuid4(),
            "user_id": user_uuid,
            "prompt": payload.prompt,
            "image_url": f"data:image/png;base64,{image_b64}",
            "format": "PNG",
            "created_at": created_at,
        }

    # Store design in DB
    design = Design(
        user_id=getattr(current_user, "id", None) or current_user.get("id") or current_user.get("sub"),
        prompt=payload.prompt,
        image_data=image_bytes,
        format="PNG",
    )
    db.add(design)
    await db.commit()
    await db.refresh(design)

    # Return with base64 encoded image for display
    return {
        "id": design.id,
        "user_id": design.user_id,
        "prompt": design.prompt,
        "image_url": f"data:image/png;base64,{image_b64}",
        "format": design.format,
        "created_at": design.created_at,
    }

@router.get("/my-designs", response_model=list[DesignResponse])
async def list_user_designs(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_active_user)):
    """List all designs created by current user."""
    if db is None:
        return []

    result = await db.execute(select(Design).where(Design.user_id == current_user.id).order_by(Design.created_at.desc()))
    designs = result.scalars().all()
    items = []
    for d in designs:
        if d.image_data:
            image_b64 = base64.b64encode(d.image_data).decode()
            url = f"data:image/png;base64,{image_b64}"
        else:
            url = d.image_url
        items.append({
            "id": d.id,
            "user_id": d.user_id,
            "prompt": d.prompt,
            "image_url": url,
            "format": d.format,
            "created_at": d.created_at,
        })
    return items

@router.get("/{design_id}", response_model=DesignResponse)
async def get_design(design_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_active_user)):
    """Get a design by ID."""
    if db is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable")

    design = await db.get(Design, UUID(design_id))
    if not design:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Design not found")
    if design.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    if design.image_data:
        image_b64 = base64.b64encode(design.image_data).decode()
        url = f"data:image/{design.format.lower()};base64,{image_b64}"
    else:
        url = design.image_url
    
    return {
        "id": design.id,
        "user_id": design.user_id,
        "prompt": design.prompt,
        "image_url": url,
        "format": design.format,
        "created_at": design.created_at,
    }

@router.post("/{design_id}/export")
async def export_design(design_id: str, payload: DesignExport, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_active_user)):
    """Export design in a specific format (PNG, JPEG, WebP, etc.)."""
    if db is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable")

    design = await db.get(Design, UUID(design_id))
    if not design:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Design not found")
    if design.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    if not design.image_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Design has no image data")
    
    # Convert to requested format
    target_format = payload.format.upper()
    if target_format == "JPG":
        target_format = "JPEG"
    
    converted = convert_image_format(design.image_data, design.format, target_format)
    if not converted:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to convert image format")
    
    # Return as downloadable file
    media_type = f"image/{target_format.lower()}"
    if target_format == "JPEG":
        media_type = "image/jpeg"
    
    return Response(
        content=converted,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename=design.{target_format.lower()}"}
    )

@router.post("/{design_id}/send-to-printer")
async def send_design_to_printer(design_id: str, payload: SendToPrinter, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_active_user)):
    """Send a design to a printer and create an order for negotiation."""
    if db is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable")

    design = await db.get(Design, UUID(design_id))
    if not design:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Design not found")
    if design.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    # Create an order for this design
    from uuid import uuid4
    order = Order(
        customer_id=current_user.id,
        print_shop_id=UUID(payload.printer_id) if payload.printer_id else None,
        product_type="CUSTOM_DESIGN",
        description=f"Custom design: {design.prompt}",
        quantity=1,
        file_url=f"data:image/png;base64,{base64.b64encode(design.image_data).decode()}",
        design_prompt=design.prompt,
        unit_price=0,  # to be negotiated
        total_price=0,  # to be negotiated
        delivery_address="TBD",
        delivery_fee=0,
        status="PENDING_NEGOTIATION",
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    
    return {
        "order_id": str(order.id),
        "status": "PENDING_NEGOTIATION",
        "printer_id": payload.printer_id,
        "message": "Design sent to printer for negotiation",
    }
