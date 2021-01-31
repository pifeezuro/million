from django.urls import path

from million_songs import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('view', views.view, name='view')
]
