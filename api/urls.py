from django.urls import path

from api import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('file/upload', views.UploadView.as_view(), name='upload'),
    path('video/save', views.VideoView.as_view(), name='video'),
]
