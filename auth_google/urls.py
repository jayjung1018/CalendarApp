from django.urls import path
from . import views
app_name = "auth_google"

urlpatterns = [
    path('', views.AuthView, name='authorize'),
    path('oauthcallback/', views.oAuthCallBack, name='callback'),
    path('logout/', views.logoutView, name='logout'),
]
