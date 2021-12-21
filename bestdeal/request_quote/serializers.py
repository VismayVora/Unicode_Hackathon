from django.db.models import fields
from rest_framework import serializers
from .models import *


class ItemSerializer(serializers.ModelSerializer):
    req_doc_name = serializers.ReadOnlyField(source = 'req_doc.name')
    req_doc_deadline = serializers.ReadOnlyField(source = 'req_doc.deadline')

    class Meta:
        model = Item
        fields = ['id', 'max_budget', 'name', 'description', 'quantity', 'units', 'industry_category', 'req_doc', 'req_doc_name', 'req_doc_deadline']


class RequirementsDocSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    deadline = serializers.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'])

    class Meta:
        model = RequirementsDoc
        fields = ['id','owner','name', 'created_at', 'deadline']


class QuoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    owner_name = serializers.ReadOnlyField(source='owner.name')
    #item = serializers.ReadOnlyField(source = 'item.id')
    delivery_by = serializers.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'])

    class Meta:
        model = Quote
        fields = ['id','owner', 'owner_name','created_at','updated_at','price', 'item', 'delivery_by', 'message', 'quantity_provided', 'units','selected']