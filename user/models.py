from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, nickname, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not nickname:
            raise ValueError("Nickname empty")
        if not password:
            raise ValueError("Password empty")

        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password=None):
        user = self.create_user(email, password=password, nickname=nickname)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()

    USER_LEVEL = [
        (1, "client"),
        (0, "admin"),
    ]

    username = models.CharField(max_length=128, null=True)
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    nickname = models.CharField(max_length=20, null=False, default="")
    level = models.IntegerField(
        verbose_name="사용자 레벨(client=1,admin=0)",
        default=1,
        null=False,
        choices=USER_LEVEL,
    )
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.email


class Profile(models.Model):
    nickname = models.OneToOneField(
        "User", related_name="profile", on_delete=models.CASCADE, default=""
    )
    avatar = models.FileField(upload_to="avatar", blank=True, default="")
    my_challenges = models.ManyToManyField(
        "challenge.Challenge", through="challenge.ChallengeApply"
    )
    my_certifications = models.ManyToManyField(
        "challenge.Challenge",
        through="challenge.Certification",
        related_name="profile_certifications",
    )

    def __str__(self):
        return str(self.nickname)
