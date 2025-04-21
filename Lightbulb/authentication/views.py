from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . models import LikePost, Profile, Post, Followers
from django.db.models import Q
from django.contrib.auth.decorators import login_required

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
        
        # Check if email already in use
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
@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('/login')

# Function that handles uploading of a new post
@login_required(login_url='/login')
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

@login_required(login_url='/login')
def home(request):
    # Get the currently logged-in user's Profile object
    profile = Profile.objects.get(user=request.user)
    # Retrieve a list of usernames that the current user is following
    following_users = Followers.objects.filter(follower=request.user.username).values_list('user', flat=True)
    # Get all posts created by:
    # Q is used to allow for combining multiple conditions
    post=Post.objects.filter(Q(user=request.user.username) | Q(user__in=following_users)).order_by('-created_at')
    context={
        'post': post,
        'profile': profile
    }
    return render(request, 'main.html', context)

# Function handling liking/unliking posts
@login_required(login_url='/login')
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

        # Get the page the user came from
        referer = request.META.get('HTTP_REFERER')
        if referer:
            # If there's a referer, redirect back to it
            return redirect(referer)
        else:
            # Fallback to home page if no referer
            return redirect('/#' + str(id))
    
# Function generates the user's feed showing their posts 
@login_required(login_url='/login')
def feed_view(request):
    # Get posts made by the current user 
    post = Post.objects.get(id=id)
    # Get the logged-in user's profile- for displaying
    profile = Profile.objects.get(user=request.user)
    # Send the posts and profile data to the main template
    context = {
        'post': post,
        'profile': profile,
    }

    return render(request, 'main.html', context)

# Function to explore the posts made by all users
@login_required(login_url='/login')
def explore(request):
    # Get all posts made by all users, order by newest first
    post = Post.objects.all().order_by('-created_at')
    profile = Profile.objects.get(user=request.user)
    # Send the posts and profile data to the explore template
    context={
        'post': post,
        'profile': profile,
    }

    return render(request, 'explore.html', context)

# Function to view a user's profile
@login_required(login_url='/login')
def profile(request,id_user):
    # Get the user object with the provided id 
    user_obj = User.objects.get(username=id_user)
    profile = Profile.objects.get(user=request.user)
    # Get the profile of the user whose profile is being viewed
    user_profile = Profile.objects.get(user=user_obj)
    user_posts = Post.objects.filter(user=user_obj.username).order_by('-created_at')
    # Calculating the number of posts made by the user
    user_post_length = len(user_posts)
    # Get the followers of the user whose profile is being viewed
    follower = request.user.username
    user = id_user
    if Followers.objects.filter(follower=follower, user=user).first():
        # If the user is already followed, unfollow them
        follow_unfollow = 'Unfollow'
    else:
        # If the user is not followed, follow them
        follow_unfollow = 'Follow'

    user_followers = len(Followers.objects.filter(user=id_user))
    user_following = len(Followers.objects.filter(follower=id_user))

    # Pass the context back to the template
    context = {
        'user_obj': user_obj,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'profile': profile,
        'follow_unfollow': follow_unfollow,
        'user_following': user_following,
        'user_followers': user_followers,
    }

    # Check if the logged-in user is the same as the user whose profile is being viewed
    if request.user.username == id_user:
        if request.method == 'POST':
            # If no image file is uploaded in the form, keep the existing image
            if request.FILES.get('image') == None:
                image = user_profile.profileimg
                bio = request.POST['bio']
                location = request.POST['location']
                # Update the profile with the new bio and location, but keep the old image
                user_profile.profileimg = image
                user_profile.bio = bio
                user_profile.location = location
                user_profile.save()
            # If an image file is uploaded in the form
            if request.FILES.get('image') != None:
                image = request.FILES.get('image')
                bio = request.POST['bio']
                location = request.POST['location']
                # Update the profile with the new image, bio, and location
                user_profile.profileimg = image
                user_profile.bio = bio
                user_profile.location = location
                user_profile.save()
            
            return redirect('/profile/'+id_user)
        else:
            return render(request, 'profile.html', context)
                
    return render(request, 'profile.html', context)

# Function to follow/unfollow users
def follow(request):
    if request.method == 'POST':
        # Get the username of the logged-in user
        follower = request.POST['follower']
        user = request.POST['user']

        if Followers.objects.filter(follower=follower, user=user).first():
            # If the user is already followed, unfollow them
            delete_follower = Followers.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)        
        else:
            new_follower = Followers.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)    
    else:
        return redirect('/')

# Function to delete a post
@login_required(login_url='/login')
def delete(request,id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect('/profile/'+request.user.username)

# Function to search for users
@login_required(login_url='/login')
def search_results(request):
    query = request.GET.get('qry')
    users = Profile.objects.filter(user__username__icontains=query)
    posts = Post.objects.filter(caption__icontains=query)
    # Send the context to the search results template
    context = {
        'query': query,
        'users': users,
        'posts': posts,
    }
    return render(request, 'search_user.html', context)
    

