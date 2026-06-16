from fastapi import APIRouter
from app.api.v1.routes import auth, users, orders, uploads, payments, wallet, logistics, print_shops, designs, debug, kyc, admin, notifications

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(uploads.router, prefix="/uploads", tags=["uploads"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])
api_router.include_router(wallet.router, prefix="/wallet", tags=["wallet"])
api_router.include_router(logistics.router, prefix="/logistics", tags=["logistics"])
api_router.include_router(print_shops.router, prefix="/print-shops", tags=["print_shops"])
api_router.include_router(designs.router, prefix="/designs", tags=["designs"])
api_router.include_router(debug.router, prefix="/debug", tags=["debug"])
api_router.include_router(kyc.router, prefix="/kyc", tags=["kyc"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
