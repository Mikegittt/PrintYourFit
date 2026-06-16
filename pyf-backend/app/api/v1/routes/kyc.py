"""KYC endpoints for customers and print shops."""
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.v1.deps import get_current_active_user, require_role
from app.services.kyc_service import submit_kyc, get_kyc_status, approve_kyc, reject_kyc, list_pending_kyc

router = APIRouter()


@router.post("/submit", response_model=dict)
async def submit_kyc_endpoint(payload: dict, current_user = Depends(get_current_active_user)):
    """Submit KYC information (documents, identity, etc.)."""
    user_id = current_user.id
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")
    
    # Extract KYC data from payload
    kyc_data = {
        "full_name": payload.get("full_name"),
        "phone_number": payload.get("phone_number"),
        "identification_type": payload.get("identification_type"),  # NATIONAL_ID, PASSPORT, DRIVER_LICENSE
        "identification_number": payload.get("identification_number"),
        "address": payload.get("address"),
        "date_of_birth": payload.get("date_of_birth"),
        "document_url": payload.get("document_url"),  # URL to uploaded document
    }
    
    result = await submit_kyc(user_id, kyc_data)
    return result


@router.get("/status", response_model=dict)
async def get_kyc_status_endpoint(current_user = Depends(get_current_active_user)):
    """Get KYC status for current user."""
    user_id = current_user.id
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")
    
    result = await get_kyc_status(user_id)
    return result


@router.put("/{user_id}/approve", response_model=dict, dependencies=[Depends(require_role("ADMIN"))])
async def approve_kyc_endpoint(user_id: str):
    """Approve KYC for a user (admin only)."""
    result = await approve_kyc(user_id)
    return result


@router.put("/{user_id}/reject", response_model=dict, dependencies=[Depends(require_role("ADMIN"))])
async def reject_kyc_endpoint(user_id: str, payload: dict):
    """Reject KYC for a user (admin only)."""
    reason = payload.get("reason", "Not specified")
    result = await reject_kyc(user_id, reason)
    return result


@router.get("/pending", response_model=list, dependencies=[Depends(require_role("ADMIN"))])
async def list_pending_kyc_endpoint():
    """List all pending KYC submissions (admin only)."""
    result = await list_pending_kyc()
    return result
