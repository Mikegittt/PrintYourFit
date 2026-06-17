from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

User = get_user_model()

class CsrfTokenView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        token = get_token(request)
        return Response({'csrfToken': token})


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if User.objects.filter(email__iexact=data['email']).exists():
            return Response({'detail': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            email=data['email'].lower(),
            password=data['password'],
            full_name=data['full_name'].strip(),
            role=data.get('role', 'CUSTOMER'),
            target_campus=data.get('target_campus', ''),
            referral_code=data.get('referral_code', None),
            is_active=True,
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = authenticate(request, username=data['email'].lower(), password=data['password'])
        if user is None:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        login(request, user)
        return Response(UserSerializer(user).data)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'status': 'logged_out'})

class CurrentUserView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(UserSerializer(request.user).data)
