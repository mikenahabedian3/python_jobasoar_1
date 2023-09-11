from django.shortcuts import render

def home_view(request):
    return render(request, 'UserApp/home.html')

def login_view(request):
    return render(request, 'UserApp/login.html')

def signup_view(request):
    return render(request, 'UserApp/signup.html')
