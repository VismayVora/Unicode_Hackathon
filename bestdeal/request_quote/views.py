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


class RequirementsDocView(viewsets.ModelViewSet):
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
		items_objs = Item.objects.filter(req_doc =req_doc.id)
		serializer = ItemSerializer(items_objs, many = True)
		return Response(serializer.data, status= status.HTTP_200_OK)


	def post(self, request, pk):
		req_doc = RequirementsDoc.objects.get(id= pk).id
		for i in range(len(request.data)):
			request.data[i]['req_doc'] = req_doc
		serializer = ItemSerializer(data= request.data, many=True)
		if not serializer.is_valid():
			return Response(serializer.errors, status= status.HTTP_403_FORBIDDEN)
		serializer.save()
		return Response(serializer.data, status= status.HTTP_201_CREATED)

class QuotesView(viewsets.ModelViewSet):
	queryset = Quote.objects.all()
	serializer_class = QuoteSerializer
	permission_classes = [IsVendorOrReadOnly]

	def get_queryset(self):
		queryset = Quote.objects.all()
		item_id = self.request.query_params.get('item')
		if item_id is not None:
			queryset = queryset.filter(item=item_id)
		return queryset
    	
	def perform_create(self,serializer):
		item_id = self.request.query_params.get('item')
		item = Item.objects.get(id = item_id)
		owner = Vendor.objects.get(email = self.request.user.email)
		serializer.save(owner = owner, item = item)

		