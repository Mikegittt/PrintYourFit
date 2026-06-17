import os
from django.apps import AppConfig
from django.db.models.signals import post_migrate


class PyfAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pyf_auth'

    def ready(self):
        from django.contrib.auth import get_user_model

        def create_default_admin(sender, **kwargs):
            User = get_user_model()
            email = os.environ.get('DJANGO_ADMIN_EMAIL', 'emmanueldevopsinc@gmail.com')
            password = os.environ.get('DJANGO_ADMIN_PASSWORD', 'PrintYourFit')
            if not User.objects.filter(email__iexact=email).exists():
                User.objects.create_superuser(email=email, password=password, full_name='Admin User')

        post_migrate.connect(create_default_admin, sender=self)
