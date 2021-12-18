from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from rest_framework.authtoken.models import Token

# Create your models here.
class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password instead of username.
        """
        if not email:
            raise ValueError('The Email must be set')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    username=None

    # extra fields
    email = models.EmailField(("Email Address"),primary_key=True)
    name = models.CharField()
    is_client = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]

    objects = UserManager()

    def __str__(self):
        return self.name

    @property
    def token(self):
        token = Token.objects.get(user=User.objects.get(self.id))
        return token

class Vendor(models.Model):

    phone_no = models.BigIntegerField(unique= True)
    user = models.OneToOneField(User, on_delete= models.CASCADE, primary_key= True)

    # Choices for industry categories
    CLOTH_TEXT = 'CT'
    PETROL_CHEM_PLASTIC = 'PCP'
    ELEC_COMP_TRASNPORT = 'ECT'
    FOOD_PROD = 'FP'
    METAL_MANUFACTURE = 'MM'
    WOOD_LEATHER_PAPER = 'WLP'
    INDUSTRY_CATEGORY_CHOICES = [
        (CLOTH_TEXT, 'Clothing and Textiles'),
        (PETROL_CHEM_PLASTIC, 'Petroleum, Chemicals and Plastics'),
        (ELEC_COMP_TRASNPORT, 'Electronics, Computers and Transportation'),
        (FOOD_PROD, 'Food Production'),
        (METAL_MANUFACTURE, 'Metal Manufacturing'),
        (WOOD_LEATHER_PAPER, 'Wood, Leather and Paper')
    ]

    industry_category = models.CharField(max_length=2,
        choices=INDUSTRY_CATEGORY_CHOICES,)
    