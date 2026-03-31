from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    ROLE_BUYER = "buyer"
    ROLE_VENDOR = "vendor"
    ROLE_ADMIN = "admin"
    ROLE_CHOICES = [
        (ROLE_BUYER, "Buyer"),
        (ROLE_VENDOR, "Vendor"),
        (ROLE_ADMIN, "Admin"),
    ]
    # Override email to make it unique (required for email login)

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices= ROLE_CHOICES, default=ROLE_BUYER)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank= True)
    phone = models.CharField(max_length=20, blank=True)


    # Tell Django to use email as the login field 
    USERNAME_FIELD = "email"
    # username is still required when creating via createsuperuser

    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email 
    
    @property 
    def is_vendor(self):
        return self.role == self.ROLE_VENDOR
    

    

