from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, username, password=None):
        if not email:
            raise ValueError("User Must have an Email Address")

        if not username:
            raise ValueError("User Must have an Username")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email),  # capital to small
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True

        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)

    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50, unique=True, blank=True)

    profile = models.CharField(max_length=20, default="merchant")
    otp = models.CharField(max_length=10, default=0, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def isFarmer(self):
        if self.profile == "farmer":
            return True
        else:
            return False


class FarmerProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    aadhar_number = models.CharField(max_length=12, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address_line_1 = models.CharField(max_length=100, blank=True)
    address_line_2 = models.CharField(max_length=100, blank=True)
    image = models.ImageField(blank=True, upload_to="farmerProfile/")
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    dob = models.DateField(blank=True, auto_now_add=True)
    bank_account = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.first_name

    def fullAddress(self):
        return f"{self.address_line_1} {self.address_line_2}"


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    aadhar_number = models.CharField(max_length=12, blank=True)

    phone_number = models.CharField(max_length=20, blank=True)
    address_line_1 = models.CharField(max_length=100, blank=True)
    address_line_2 = models.CharField(max_length=100, blank=True)
    image = models.ImageField(blank=True, upload_to="userProfile/")
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    dob = models.DateField(blank=True, auto_now_add=True)

    def __str__(self):
        return self.user.first_name

    def fullAddress(self):
        return f"{self.address_line_1} {self.address_line_2}"
