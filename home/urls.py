from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.register, name='register'),
    path('register', views.register, name='register'),
    path('login', views.login, name="login"),
    path('logs', views.logs, name="logs"),
    path('live', views.live, name="live"),
    path('live_classification', views.live_classification,
         name="live_classification"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('signup', views.Register, name="signup"),
    path('Login', views.Login, name="Login"),
    path('Classify', views.Classify, name="Classify"),
    path('load_video', views.load_video, name="load_video"),
    path('Logout', views.Logout, name="Logout"),
    path('assign_value', views.assign_value, name="assign_value"),
    path('write_to_json', views.write_to_json, name="write_to_json"),
    path('send_json', views.send_json, name="send_json")
]
