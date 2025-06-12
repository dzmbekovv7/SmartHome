from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission
import random
import string
from django.contrib.auth.models import AbstractUser

class UserManager(models.Manager):
    def get_by_natural_key(self, email):
        return self.get(email=email)

    def create_user(self, username, email, password=None, phone=None, confirmation_code=None, **extra_fields):
        if confirmation_code is None:
            confirmation_code = ''.join(random.choices(string.digits, k=6))
        user = self.model(username=username, email=email, phone=phone, confirmation_code=confirmation_code,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, phone=None, confirmation_code=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(username, email, password, phone, confirmation_code, **extra_fields)
class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    password = models.CharField(max_length=128)
    is_superuser = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    role = models.CharField(max_length=10, default='user')  # новое поле

    reset_code = models.CharField(max_length=6, blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=6, blank=True, null=True)
    is_online = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    is_actively_looking = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users'

    def save(self, *args, **kwargs):
        # обновляем role в зависимости от is_superuser и is_agent
        if self.is_superuser:
            self.role = 'admin'
        elif self.is_agent:
            self.role = 'agent'
        else:
            self.role = 'user'

        if not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def save(self, *args, **kwargs):
        if not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_staff(self):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

    def get_username(self):
        return self.username

    def check_password(self, raw_password):
        return make_password(raw_password) == self.password