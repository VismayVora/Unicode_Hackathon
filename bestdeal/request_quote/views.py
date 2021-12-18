from django.shortcuts import render
from rest_framework import viewsets,permissions
from .models import RequirementsDoc,Item,Quote
from .serializers import RequirementsDocSerializer,ItemSerializer,QuoteSerializer

# Create your views here.
class ItemDetails(viewsets.ModelViewSet):
	queryset = Item.objects.all()
	serializer_class = ItemSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Item.objects.filter(owner=self.request.user)
	
	def perform_create(self,serializer):
		serializer.save(owner = self.request.user)
	
	#def update(self, request, *args, **kwargs):
		#kwargs['partial'] = True
		#return super().update(request, *args, **kwargs)