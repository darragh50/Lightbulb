from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static 
from django.conf import settings
from authentication import views

urlpatterns = [
    path('admin/', admin.site.urls), # Route for the Django admin site
    path('',views.home), # Home page
    path('signup/', views.signup), # Route for the signup page
    path('login/', views.login_view), # Route for the login page
    path('logout/', views.logout_view), # Route for the logout page
    path('upload/', views.upload), # Route to upload a new post 
    path('like-post/<str:id>', views.like, name='like-post'), # Route to like a post — expects a string 'id' in the URL to identify the post
    path('#<str:id>', views.feed_view), # Redirect route to a post on the homepage using an id (#)
    path('explore', views.explore), # Route for the explore page
    path('profile/<str:id_user>', views.profile), # User profile page — expects a string 'id_user' in the URL to identify the profile owner
    path('follow', views.follow, name='follow'), # Route to follow a user
    path('delete/<str:id>', views.delete, name='delete'), # Delete a post — expects a string 'id' in the URL to identify the post to delete
    path('search-results/', views.search_results, name='search_results'), # Route for search results
]


