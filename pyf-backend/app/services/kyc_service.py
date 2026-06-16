"""KYC (Know Your Customer) service for customers and print shops."""
from datetime import datetime, timedelta
from uuid import UUID

# In-memory KYC submissions storage (in production, this would be in a database)
_kyc_submissions: dict[str, dict] = {}


async def submit_kyc(user_id: str | UUID, kyc_data: dict) -> dict:
    """Submit or update KYC for a user or print shop."""
    user_id_str = str(user_id)
    _kyc_submissions[user_id_str] = {
        "user_id": user_id_str,
        "data": kyc_data,
        "submitted_at": datetime.utcnow().isoformat(),
        "status": "PENDING",  # PENDING, APPROVED, REJECTED
    }
    return {
        "user_id": user_id_str,
        "status": "PENDING",
        "message": "KYC submitted successfully. Admin will review within 2-3 business days."
    }


async def get_kyc_status(user_id: str | UUID) -> dict:
    """Get KYC status for a user or print shop."""
    user_id_str = str(user_id)
    submission = _kyc_submissions.get(user_id_str)
    
    if not submission:
        return {
            "user_id": user_id_str,
            "status": "NOT_SUBMITTED",
            "message": "KYC not yet submitted."
        }
    
    return {
        "user_id": user_id_str,
        "status": submission["status"],
        "submitted_at": submission["submitted_at"],
        "message": f"KYC status: {submission['status']}"
    }


async def approve_kyc(user_id: str | UUID) -> dict:
    """Approve KYC for a user (admin only)."""
    user_id_str = str(user_id)
    submission = _kyc_submissions.get(user_id_str)
    
    if not submission:
        return {
            "user_id": user_id_str,
            "status": "NOT_FOUND",
            "message": "No KYC submission found for this user."
        }
    
    submission["status"] = "APPROVED"
    submission["approved_at"] = datetime.utcnow().isoformat()
    
    return {
        "user_id": user_id_str,
        "status": "APPROVED",
        "message": "KYC approved successfully."
    }


async def reject_kyc(user_id: str | UUID, reason: str = None) -> dict:
    """Reject KYC for a user (admin only)."""
    user_id_str = str(user_id)
    submission = _kyc_submissions.get(user_id_str)
    
    if not submission:
        return {
            "user_id": user_id_str,
            "status": "NOT_FOUND",
            "message": "No KYC submission found for this user."
        }
    
    submission["status"] = "REJECTED"
    submission["rejected_at"] = datetime.utcnow().isoformat()
    submission["rejection_reason"] = reason
    
    return {
        "user_id": user_id_str,
        "status": "REJECTED",
        "message": f"KYC rejected. Reason: {reason or 'Not specified'}"
    }


async def list_pending_kyc() -> list[dict]:
    """List all pending KYC submissions (admin only)."""
    pending = []
    for user_id, submission in _kyc_submissions.items():
        if submission["status"] == "PENDING":
            pending.append({
                "user_id": user_id,
                "submitted_at": submission["submitted_at"],
                "data": submission["data"]
            })
    return pending
