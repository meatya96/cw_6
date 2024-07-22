from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager

NULLABLE = {'blank': True, 'null': True}
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=100, verbose_name='Отчество', **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='почта')
    message = models.TextField(verbose_name='Комментарий',  **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()  # Указываем наш новый UserManager

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


# Добавление или изменение related_name для поля groups
User.groups.field.remote_field.related_name = 'custom_user_groups'

# Добавление или изменение related_name для поля user_permissions
User.user_permissions.field.remote_field.related_name = 'custom_user_permissions'
