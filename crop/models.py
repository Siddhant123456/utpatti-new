from django.db import models
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

from account.models import FarmerProfile,UserProfile


class Crop(models.Model):
    crop_name = models.CharField(max_length=20)
    farmer = models.ForeignKey(FarmerProfile,on_delete=models.CASCADE)
    crop_desc = models.TextField()
    class Seasons(models.TextChoices):
        RABI = 'Rabi'
        KHARIF = 'Kharif'

    season = models.CharField(choices=Seasons.choices, max_length=15,default="")
    slug = models.SlugField(blank=True,max_length=255)
    stock = models.IntegerField()
    price = models.IntegerField()
    is_available = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.crop_name

    def getBid(self):
        try:
            self.bid
        except ObjectDoesNotExist:
            return False


class MerchantCrop(models.Model):
    merchant = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop,on_delete=models.DO_NOTHING)

    #payment field will be added here 








