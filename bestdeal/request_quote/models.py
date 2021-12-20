from django.db import models
from django.db.models.fields import DateTimeField
from django.conf import settings

from accounts.models import Vendor

# Create your models here.

class RequirementsDoc(models.Model):

    #Foreign Keys
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    # Adding Fields related to the request for quotations doc
    name = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    deadline = models.DateField()

    def __str__(self):
        return self.name

class Item(models.Model):
    
    # Adding Fields related to the Items doc
    max_budget = models.BigIntegerField()  
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField()
    units = models.CharField(max_length=20)

    # Foreign keys
    req_doc = models.ForeignKey(RequirementsDoc, on_delete= models.CASCADE)

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

    industry_category = models.CharField(max_length=3,
        choices=INDUSTRY_CATEGORY_CHOICES)

class Quote(models.Model):

    # Foreign keys
    item = models.ForeignKey(Item, on_delete= models.CASCADE)
    owner=models.ForeignKey(Vendor,on_delete=models.CASCADE)

    # Other fields related to Quote
    price = models.BigIntegerField()
    delivery_by = models.DateField()
    quantity_provided = models.IntegerField()
    units = models.CharField(max_length=20)
    message = models.CharField(max_length=200, blank= True, null= True)
    created_at = models.DateField(auto_now_add=True, null = True)
    updated_at = models.DateField(auto_now=True, null = True)
    selected = models.BooleanField(default=False)

    class Meta:
        unique_together = ['item', 'owner']