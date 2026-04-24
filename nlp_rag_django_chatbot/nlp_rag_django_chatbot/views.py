import json
from django.http import JsonResponse
from django.shortcuts import render

def home(request):
    return render(request, 'query/home.html')