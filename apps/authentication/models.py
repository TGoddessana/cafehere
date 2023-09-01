from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.utils.models import TimeStampedMixin, UUID4Mixin
from core.utils.validators import validate_mobile_number


class UserManager(BaseUserManager):
    def create_user(self, mobile, password=None):
        user: User = self.model(mobile=mobile)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile: str, password=None):
        user: User = self.create_user(mobile=mobile, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, UUID4Mixin, TimeStampedMixin, PermissionsMixin):
    USERNAME_FIELD = "mobile"
    objects = UserManager()

    mobile = models.CharField(
        max_length=18, validators=[validate_mobile_number], unique=True
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_("Designates whether this user should be treated as active."),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    def __str__(self) -> str:
        return f"User {self.mobile}"
