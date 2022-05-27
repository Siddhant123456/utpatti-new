from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render



def home(request):
    return render(request,'home.html')