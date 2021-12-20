from re import S
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from rest_framework import viewsets,permissions
from rest_framework.decorators import permission_classes
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from accounts.models import Vendor

from .custompermissions import IsClientOrReadOnly, IsVendorOrReadOnly
from .models import RequirementsDoc,Item,Quote
from .serializers import RequirementsDocSerializer,ItemSerializer,QuoteSerializer
from .whatsapp import send_message

from rest_framework.response import Response
from rest_framework import status

import datetime
from django.http import JsonResponse


class RequirementsDocView(viewsets.ModelViewSet):
	permission_classes = [IsClientOrReadOnly]
	queryset = RequirementsDoc.objects.all()
	serializer_class = RequirementsDocSerializer
	
	def get_queryset(self):
		return RequirementsDoc.objects.filter(owner = self.request.user)
		
	def perform_create(self,serializer):
	    serializer.save(owner = self.request.user)


class ItemsAPI(APIView):
	permission_classes = [IsClientOrReadOnly]

	def get(self, request, pk):
		req_doc = RequirementsDoc.objects.get(id= pk)
		if(self.request.user.is_client == False and datetime.date.today() - req_doc.deadline > datetime.timedelta(0)):
			return JsonResponse({"Message": "The deadline to provide quotations for this document has passed!"})
		else:
			items_objs = Item.objects.filter(req_doc =req_doc.id)
			serializer = ItemSerializer(items_objs, many = True)
			return Response(serializer.data, status= status.HTTP_200_OK)

	def post(self, request, pk):
		req_doc = RequirementsDoc.objects.get(id= pk)
		for i in range(len(request.data)):
			request.data[i]['req_doc'] = req_doc.id
		serializer = ItemSerializer(data= request.data, many=True)
		if not serializer.is_valid():
			return Response(serializer.errors, status= status.HTTP_403_FORBIDDEN)
		serializer.save(req_doc = req_doc)
		industries = []
		vendors_list = []
		for i in range(len(request.data)):
			industries.append(request.data[i]['industry_category'])
		print(industries)
		for industry in industries:
			vendors = Vendor.objects.filter(industry_category=industry)
			vendors_list.append(vendors)
		print(vendors_list)
		for vendors in vendors_list:
			for vendor in vendors:
				print(vendor)
				send_message(request, vendor)
		return Response(serializer.data, status= status.HTTP_201_CREATED)

class VendorQuotesView(viewsets.ModelViewSet):
	queryset = Quote.objects.all()
	serializer_class = QuoteSerializer
	permission_classes = [IsVendorOrReadOnly]

	def get_queryset(self):
		if self.request.user.is_vendor:
			queryset = Quote.objects.filter(owner = self.request.user)
		return queryset
    	
	def perform_create(self,serializer):
		owner = Vendor.objects.get(email = self.request.user.email)
		serializer.save(owner = owner)

