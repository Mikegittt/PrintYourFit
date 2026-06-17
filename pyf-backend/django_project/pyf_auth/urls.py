from django.urls import path
from .views import CsrfTokenView, RegisterView, LoginView, LogoutView, CurrentUserView

urlpatterns = [
    path('auth/csrf/', CsrfTokenView.as_view(), name='csrf-token'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('users/me/', CurrentUserView.as_view(), name='current-user'),
]
