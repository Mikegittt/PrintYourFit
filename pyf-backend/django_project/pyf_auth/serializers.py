from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    referred_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'full_name',
            'email',
            'role',
            'target_campus',
            'referral_code',
            'referred_by',
            'kyc_completed',
            'kyc_completed_at',
            'is_active',
            'created_at',
        ]

class RegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=128)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(max_length=32)
    target_campus = serializers.CharField(max_length=64, required=False, allow_blank=True)
    referral_code = serializers.CharField(max_length=32, required=False, allow_blank=True)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
