from django.shortcuts import render, redirect 
from .forms import *
# Create your views here.

def home(request):
    return render(request, "pages/landing.html", {})

def upload_image(request): 
    return render(request, 'pages/image_upload.html') 

def login(request):
    return render(request, 'pages/login.html')

def select(request):
    return render(request, 'pages/select.html')

def ocr(request):
    return render(request, 'pages/ocr.html') 

def profile(request):
    return render(request, 'pages/profile.html') 