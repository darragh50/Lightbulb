from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . models import LikePost, Profile, Post

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
            return redirect('/login')
        
        except Exception as e:
            return render(request, 'signup.html', {'invalid': f"Error: {str(e)}"})

    return render(request, 'signup.html')

# Function to handle user login
def login_view(request):
    if request.method == 'POST':
        firstname =request.POST.get('firstname')
        password =request.POST.get('password')
        # Checks if a user exists with the given credentials
        user=authenticate(request,username=firstname, password=password)
      
        # Redirect depending on if successful or not
        if user is not None:
            login(request, user)
            return redirect('/')
        invalid="Invalid Credentials"

        return render(request, 'login.html', {'invalid':invalid})
    
    return render(request, 'login.html')

# Function to handle user logout
def logout_view(request):
    logout(request)
    return redirect('/login')

# Function that handles uploading of a new post
def upload(request):
    if request.method == 'POST':
        # Get user, image and caption from the form 
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        # Creates a new post object and saves it
        new_post=Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')


def home(request):
    post=Post.objects.all().order_by('created_at')
    context={
        'post': post,
    }
    return render(request, 'main.html', context)

# Function handling liking/unliking posts
def like(request,id):
    if request.method == 'GET':
        
        # Get the username of the logged in user
        username = request.user.username
        # Fetch the post from the database using the given id
        # If the post doesn't exist - return a 404 error
        post = get_object_or_404(Post, id=id)

        # Check if the user has already liked the post
        like_filter = LikePost.objects.filter(post_id=post.id, username=username).first()
        # Increase like count/decrease depending on status of the user
        if like_filter is None:
            new_like = LikePost.objects.create(post_id=post.id, username=username)
            post.numLikes = post.numLikes + 1

        else:
            like_filter.delete()
            post.numLikes = post.numLikes - 1

        post.save()

        return redirect('/')