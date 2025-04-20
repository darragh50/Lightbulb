from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static 
from django.conf import settings
from authentication import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('signup/', views.signup),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('upload/', views.upload),
    path('like-post/<str:id>', views.like, name='like-post'),
    path('#<str:id>', views.feed_view),
    path('explore', views.explore),
    path('profile/<str:id_user>', views.profile),
    path('follow', views.follow, name='follow'),
    path('delete/<str:id>', views.delete, name='delete'),
    path('search-results/', views.search_results, name='search_results'),
]


