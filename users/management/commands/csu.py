from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.create_user(
            email='admin@sky.pro',
            phone='1234',
            password='1234',
            is_staff=True,
            is_superuser=True
        )

        self.create_user(
            email='user@sky.pro',
            phone='5678',
            password='1234',
            is_staff=False,
            is_superuser=False
        )

    def create_user(self, email, phone, password, is_staff, is_superuser):
        user = User.objects.create(
            email=email,
            phone=phone,
            is_staff=is_staff,
            is_superuser=is_superuser
        )
        user.set_password(password)
        user.save()
        self.stdout.write(self.style.SUCCESS(f'Пользователь {email} успешно создан.'))
