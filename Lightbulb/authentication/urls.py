from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static 
from django.conf import settings
from authentication import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('signup/', views.signup, name='signup')
]


