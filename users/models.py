from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        # Send error when either one of the fields is empty or both are empty
        if not email:
            raise ValueError("User must have an email!")
        
        if not password:
            raise ValueError("User must have a password!")
        
        user = self.model(
            email=self.normalize_email(email),
        )
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password,
        )
        
        # Add admin attributes to user
        user.is_superuser = True
        user.is_staff = True
        
        user.save(using=self._db)
        
        return user
        
        
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="Email address",
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    # Connect UserManager with User
    objects = UserManager()
    
    def __str__(self):
        return self.email
    

# Profile
class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name="profile",
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)