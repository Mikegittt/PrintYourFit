from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import PrintShop, Order, Logistics, CashoutRequest, PointsLedger, Notification

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'role', 'is_active', 'is_staff', 'kyc_completed', 'created_at')
    list_filter = ('role', 'is_active', 'is_staff', 'kyc_completed')
    search_fields = ('email', 'full_name', 'referral_code')
    readonly_fields = ('id', 'created_at')
    ordering = ('-created_at',)


@admin.register(PrintShop)
class PrintShopAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'user_id', 'status', 'is_verified', 'kyc_completed', 'approved_at', 'created_at')
    list_filter = ('status', 'is_verified', 'kyc_completed')
    search_fields = ('shop_name', 'whatsapp_number')
    readonly_fields = ('id', 'created_at', 'approved_at')
    ordering = ('-created_at',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product_type', 'customer_id', 'print_shop_id', 'status', 'total_price', 'delivery_address', 'created_at')
    list_filter = ('status',)
    search_fields = ('product_type', 'file_url', 'payment_reference')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(Logistics)
class LogisticsAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'dispatcher_name', 'dispatched_at', 'estimated_delivery', 'delivered_at')
    search_fields = ('dispatcher_name', 'tracking_notes')
    readonly_fields = ('id',)
    ordering = ('-dispatched_at',)


@admin.register(CashoutRequest)
class CashoutRequestAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'points_amount', 'naira_value', 'channel', 'status', 'created_at')
    list_filter = ('status', 'channel')
    search_fields = ('destination',)
    readonly_fields = ('id', 'created_at')
    ordering = ('-created_at',)


@admin.register(PointsLedger)
class PointsLedgerAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'points_delta', 'fiat_equivalent', 'transaction_type', 'order_id', 'created_at')
    list_filter = ('transaction_type',)
    readonly_fields = ('id', 'created_at')
    ordering = ('-created_at',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'source', 'created_at')
    list_filter = ('active', 'source')
    search_fields = ('title', 'message', 'source')
    readonly_fields = ('id', 'created_at')
    ordering = ('-created_at',)
