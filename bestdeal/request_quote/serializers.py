from django.db.models import fields
from rest_framework import serializers
from .models import *


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'max_budget', 'name', 'description', 'quantity', 'units', 'industry_category', 'req_doc']


class RequirementsDocSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = RequirementsDoc
        fields = ['id','owner','name', 'created_at', 'deadline']


class QuoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Quote
        fields = ['id','owner','created_at','updated_at','price', 'item', 'delivery_by', 'message', 'quantity_provided', 'units']