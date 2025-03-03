from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . models import Profile

# Create your views here.
# Handle user registration - check request method. Recieve and save user input to user model
def signup(request):
    try:
     if request.method == 'POST':
        firstname = request.POST.get('firstname')
        emailID = request.POST.get('emailID')
        password = request.POST.get('password')

        my_user = User.objects.create_user(firstname, emailID, password)
        my_user.save()

        user_model = User.objects.get(username=firstname)
        new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
        new_profile.save()

        if my_user is not None:
           login(request, my_user)
           return redirect('/')
        return redirect('/')
    
    except:
       invalid="User already exists"
       return render(request, 'signup.html', {'invalid':invalid})

def home(request):
    return HttpResponse("Test")