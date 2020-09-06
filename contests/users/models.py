from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name = "profile")
    name = models.CharField(max_length=30,blank=True)

    codeChef = models.BooleanField(default=True)
    codeForces = models.BooleanField(default=True)
    hackerEarth = models.BooleanField(default=True)
    hackerRank = models.BooleanField(default=True)
    spoj = models.BooleanField(default=True)

    @property
    def get_email(self):
        return self.user.email

    def get_sites(self):
        return [self.codeChef, self.codeForces, self.hackerEarth, self.hackerRank, self.spoj]

    def get_name(self):
        return self.name

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = ("Profile")
        verbose_name_plural = ("Profiles")
        ordering = ("user",)


@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender,created,instance,**kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()