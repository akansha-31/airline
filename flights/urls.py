from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("index", views.index, name="index"),
    path('accounts/', include('django.contrib.auth.urls')),
    path("register", views.register_view, name="register"),
    path("profile", views.profile, name="profile"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("<int:flight_id>", views.flight, name="flight"), # if someone types an integer we will call it flight_id then the function i want to run is views.flight
    path("<int:flight_id>/book", views.book, name="book"),
]

