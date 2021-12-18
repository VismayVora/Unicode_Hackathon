from django.db.models import fields
from rest_framework import serializers
from .models import *

class RequirementsDocSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    class Meta:
        model = RequirementsDoc
        fields = ['owner','name', 'created_at', 'updated_at', 'deadline']


class ItemSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    class Meta:
        model = Item
        fields = ['owner','max_budget', 'name', 'description', 'quantity', 'units', 'req_doc', 'industry_category']


class QuoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    class Meta:
        model = Quote
        fields = ['owner','price', 'item', 'delivery_by', 'message', 'quantity_provided', 'units']