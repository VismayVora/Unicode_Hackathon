from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from .serializers import ClientRegisterSerializer,VendorRegisterSerializer,LoginSerializer
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.contrib.auth import authenticate,login

from rest_framework.response import Response
from rest_framework import status,permissions

from .models import User

# Create your views here.
class ClientRegisterAPI(GenericAPIView):
	permission_classes = [permissions.AllowAny]
	
	serializer_class = ClientRegisterSerializer
	
	def post(self,request,*args,**kwargs):
		data = request.data
		serializer = self.serializer_class(data=data)
		serializer.is_valid(raise_exception = True)
		user = serializer.save()
		token = Token.objects.create(user=user)
		current_site = get_current_site(request).domain
		relative_link = reverse('email-verify')
		link = 'http://'+current_site+relative_link+'?token='+ token.key
		data = {'email_body': f'Use this link to get verified {link}.', 'subject':'Email Verification', 'to' : user.email}
		Util.send_email(data)
		return Response({'Success':'Your account is successfully created,please check your mail for verification.'},status=status.HTTP_201_CREATED)

class VendorRegisterAPI(GenericAPIView):
	permission_classes = [permissions.AllowAny]
	
	serializer_class = VendorRegisterSerializer
	
	def post(self,request,*args,**kwargs):
		data = request.data
		serializer = self.serializer_class(data=data)
		serializer.is_valid(raise_exception = True)
		user = serializer.save()
		token = Token.objects.create(user=user)
		current_site = get_current_site(request).domain
		relative_link = reverse('email-verify')
		link = 'http://'+current_site+relative_link+'?token='+ token.key
		data = {'email_body': f'Use this link to get verified {link}.', 'subject':'Email Verification', 'to' : user.email}
		Util.send_email(data)
		return Response({'Success':'Your account is successfully created,please check your mail for verification.'},status=status.HTTP_201_CREATED)

class LoginAPI(GenericAPIView):
	permission_classes = [permissions.AllowAny]
	serializer_class = LoginSerializer
	
	def post(self,request,*args,**kwargs ):
		email = request.data.get('email',None)
		password = request.data.get('password',None)
		user = authenticate(email = email, password = password)
		if user :
			login(request,user)
			serializer = self.serializer_class(user)
			token = Token.objects.get(user=user)
			return Response({'token' : token.key,'email' : user.email},status = status.HTTP_200_OK)
		return Response('Invalid Credentials',status = status.HTTP_404_NOT_FOUND)

class EmailVerify(GenericAPIView):
	permission_classes = [permissions.AllowAny]
	def get(self,request):
		token = request.GET.get('token')
		user = User.objects.get(auth_token = token)
		if not user.is_active:
			user.is_active = True
			user.save()
		return Response('Account Verified', status=status.HTTP_200_OK)