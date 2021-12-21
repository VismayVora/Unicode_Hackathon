from re import S
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from rest_framework import viewsets,permissions
from rest_framework.decorators import permission_classes
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from accounts.models import Vendor

from .custompermissions import IsClientOrReadOnly, IsVendor,IsClient
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
			#Ensures that a vendor only gets to see the items in the rquirements doc if the deadline has not passed.
			return JsonResponse({"Message": "The deadline to provide quotations for this document has passed!"})
		else:
			items_objs = Item.objects.filter(req_doc =req_doc.id)
			serializer = ItemSerializer(items_objs, many = True)
			return Response(serializer.data, status= status.HTTP_200_OK)

	def post(self, request, pk):
		req_doc = RequirementsDoc.objects.get(id= pk)
		for i in range(len(request.data)):
			request.data[i]['req_doc'] = pk  # Linking the item to the current req_doc by adding its pk.
		serializer = ItemSerializer(data= request.data, many=True)
		if not serializer.is_valid():
			return Response(serializer.errors, status= status.HTTP_403_FORBIDDEN)
		serializer.save(req_doc = req_doc)

		industries = []  # Created an empty list to filter the vendors against the industry to which the item belongs
		vendors_list = [] # Filtered vendors will be stored in this list.

		for i in range(len(request.data)):
			industries.append(request.data[i]['industry_category'])
		
		for industry in industries:
			vendors = Vendor.objects.filter(industry_category=industry)
			vendors_list.append(vendors)

		for vendors in vendors_list:
			for vendor in vendors:
				print(vendor)
				send_message(request, vendor)
				
		return Response(serializer.data, status= status.HTTP_201_CREATED)

class VendorQuotesView(viewsets.ModelViewSet):
	queryset = Quote.objects.all()
	serializer_class = QuoteSerializer
	permission_classes = [IsVendor]

	def get_queryset(self):
		queryset = Quote.objects.filter(owner = self.request.user)
		return queryset
    	
	def perform_create(self,serializer):
		owner = Vendor.objects.get(email = self.request.user.email)
		serializer.save(owner = owner)


# class VendorQuotesView(APIView):		
# 	permission_classes = [IsVendor]

# 	def get(self, request, pk):
# 		quote_objs = Quote.objects.filter(owner = self.request.user).filter(item__req_doc = pk)
# 		serializer = QuoteSerializer(quote_objs, many = True)
# 		return Response(serializer.data, status= status.HTTP_200_OK)

# 	def post(self, request, pk):
# 		owner = Vendor.objects.get(email = self.request.user.email)
# 		serializer = ItemSerializer(data= request.data, many=True)
# 		serializer.save(owner = owner, item = pk)


class ClientQuotesView(APIView):
	permission_classes = [IsClient]
	
	def get(self,request,pk):
		quote_objs = Quote.objects.filter(item__req_doc=pk)
		serializer = QuoteSerializer(quote_objs, many = True)
		return Response(serializer.data, status= status.HTTP_200_OK)
	
	def patch(self,request):
		data = request.data
		quote_obj = Quote.objects.get(id = data['id'])
		serializer = QuoteSerializer(quote_obj,data=data,partial=True)
		if serializer.is_valid():
			serializer.save()
		return Response(serializer.data, status= status.HTTP_201_CREATED)

class FinalList(APIView):

	def get(self, request, pk):
		quotes_objs = Quote.objects.filter(item__req_doc = pk).filter(selected = True)
		serializer = QuoteSerializer(quotes_objs, many = True)
		return Response(serializer.data, status= status.HTTP_200_OK)