import uuid
import random
import string
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


def generate_referral_code(length: int = 8) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(random.choice(alphabet) for _ in range(length))


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, full_name, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('role') in [None, 'AMBASSADOR']:
            extra_fields['role'] = 'CUSTOMER'
        if extra_fields.get('role') == 'CUSTOMER' and not extra_fields.get('referral_code'):
            extra_fields['referral_code'] = generate_referral_code()
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, full_name='', **extra_fields):
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, full_name, **extra_fields)

    def create_superuser(self, email, password, full_name='', **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, full_name, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=32, default='CUSTOMER')
    referral_code = models.CharField(max_length=32, unique=True, null=True, blank=True)
    referred_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='referred_users')
    target_campus = models.CharField(max_length=64, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    kyc_completed = models.BooleanField(default=False)
    kyc_completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email


class PrintShop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField()
    shop_name = models.CharField(max_length=128)
    address = models.TextField()
    state = models.CharField(max_length=64)
    whatsapp_number = models.CharField(max_length=20)
    status = models.CharField(max_length=32, default='PENDING')
    is_verified = models.BooleanField(default=False)
    kyc_completed = models.BooleanField(default=False)
    kyc_completed_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'print_shops'
        managed = False


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_id = models.UUIDField()
    print_shop_id = models.UUIDField()
    referred_by = models.UUIDField(null=True, blank=True)
    product_type = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField()
    file_url = models.TextField(null=True, blank=True)
    design_prompt = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=32, default='PENDING')
    delivery_address = models.TextField()
    delivery_fee = models.DecimalField(max_digits=12, decimal_places=2)
    payment_reference = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'orders'
        managed = False


class Logistics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.UUIDField()
    dispatcher_name = models.CharField(max_length=128, null=True, blank=True)
    tracking_notes = models.TextField(null=True, blank=True)
    dispatched_at = models.DateTimeField(null=True, blank=True)
    estimated_delivery = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'logistics'
        managed = False


class CashoutRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField()
    points_amount = models.IntegerField()
    naira_value = models.DecimalField(max_digits=12, decimal_places=2)
    channel = models.CharField(max_length=32)
    destination = models.CharField(max_length=128)
    status = models.CharField(max_length=32, default='PENDING')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'cashout_requests'
        managed = False


class PointsLedger(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.UUIDField()
    points_delta = models.IntegerField()
    fiat_equivalent = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=32)
    order_id = models.UUIDField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'points_ledger'
        managed = False


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    message = models.CharField(max_length=2000)
    created_at = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    source = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        db_table = 'notifications'
        managed = False
