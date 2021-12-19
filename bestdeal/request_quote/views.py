from re import S
from django.shortcuts import render
from rest_framework import viewsets,permissions
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from .models import RequirementsDoc,Item,Quote
from .serializers import RequirementsDocSerializer,ItemSerializer,QuoteSerializer

from rest_framework.response import Response
from rest_framework import status


class RequirementsDocView(viewsets.ModelViewSet):
    queryset = RequirementsDoc.objects.all()
    serializer_class = RequirementsDocSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RequirementsDoc.objects.filter(owner = self.request.user)
    
    def perform_create(self,serializer):
	    serializer.save(owner = self.request.user)


class ItemsAPI(APIView):

	def get(self, request, pk):
		req_doc = RequirementsDoc.objects.get(id= pk)
		items_objs = Item.objects.filter(req_doc =req_doc.id)
		serializer = ItemSerializer(items_objs, many = True)
		return Response(serializer.data, status= status.HTTP_200_OK)


	def post(self, request, pk):
		request.data['req_doc'] = RequirementsDoc.objects.get(id= pk).id
		serializer = ItemSerializer(data= request.data)
		if not serializer.is_valid():
			return Response(serializer.errors, status= status.HTTP_403_FORBIDDEN)
		serializer.save()
		return Response(serializer.data, status= status.HTTP_201_CREATED)