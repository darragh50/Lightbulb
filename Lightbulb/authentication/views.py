from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . models import Profile

# Create your views here.
# Handle user registration - check request method. Recieve and save user input to user model
def signup(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        emailID = request.POST.get('emailID')
        password = request.POST.get('password')
        
        # Check if user already exists
        if User.objects.filter(username=firstname).exists():
            return render(request, 'signup.html', {'invalid': "User already exists"})
        
        if User.objects.filter(email=emailID).exists():
            return render(request, 'signup.html', {'invalid': "Email already in use"})

        # Create user
        try:
            my_user = User.objects.create_user(username=firstname, email=emailID, password=password)
            my_user.save()

            # Create profile
            new_profile = Profile.objects.create(user=my_user, id_user=my_user.id)
            new_profile.save()

            # Log the user in
            login(request, my_user)
            return redirect('/')
        
        except Exception as e:
            return render(request, 'signup.html', {'invalid': f"Error: {str(e)}"})

    return render(request, 'signup.html')

def home(request):
    return HttpResponse("Home")