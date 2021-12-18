from django.db.models import fields
from rest_framework import serializers
from .models import *

class RequirementsDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequirementsDoc
        fields = ['name', 'created_at', 'updated_at', 'deadline']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['max_budget', 'name', 'description', 'quantity', 'units', 'req_doc', 'industry_category']


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ['price', 'item', 'delivery_by', 'message', 'quantity_provided', 'units']