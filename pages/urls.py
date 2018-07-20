from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('delete/<int:pk>/', views.deleteTaskView, name='delete'),
    path('removeReminder/<int:pk>/', views.removeReminder, name='removeReminder'),
    path('events/',views.getEvents,name='events')
]
