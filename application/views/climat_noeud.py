from .climat_noeud_serializers import ClimatSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from django.shortcuts import render
from rest_framework import status
from ast import literal_eval
import pyowm

@csrf_exempt
@api_view(['GET', 'POST'])
def sauvegarder_donnees_noeud(request):
	print("Arduino Message : Donnees recu")
	if request.method=='POST':
		serializer=ClimatSerializer(data=request.data)
		if serializer.is_valid():
			print("Arduino Message : Executer avec succes.")
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			print("Arduino Message : Format incorrect!")
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
