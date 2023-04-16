from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view


from .models import Company
from .serializers import CompanySerializer



@api_view(['GET'])
def companies(request):

	company = Company.objects.all()
	serializer = CompanySerializer(company, many=True)

	return Response(serializer.data)
