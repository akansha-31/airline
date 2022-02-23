from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Flight, Passenger, UserProfile
from django.urls import reverse
from django.contrib.auth.models import User
# Create your views here.
def profile(request):
    if request.method == "GET":
        context = {
            "userprofile" : UserProfile.objects.all(),
        }
        return render(request, "flights/profile.html", context)

def index(request):
    ''' 
    context dictionary is a dictionary that maintains keys and values keys as the things we want to plug in to the templates
    as the names of those things and the values are what we actually want to plug in 
    '''
    if not request.user.is_authenticated:
        return render(request, "flights/login.html", {"message":None})
    context = {
        "flights" : Flight.objects.all(),
    }
    return render(request, "flights/index.html", context) # pass context as third argument

def flight(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id) # get the flight whose number is flight id.
    except Flight.DoesNotExist:
        raise Http404("Flight does not exist.")

    context = {
        "flight" : flight,
        "passengers" :  flight.passengers.all(),
        "non_passengers" : Passenger.objects.exclude(flights=flight).all()
    }
    return render(request, "flights/flight.html", context)

def book(request, flight_id):
    try:
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
        flight = Flight.objects.get(pk=flight_id)
    except KeyError:
        return render(request, "flights/error.html", {"message" : "No selection."})
    except Flight.DoesNotExist:
        return render(request, "flights/error.html", {"message" : "No flight."})
    except Passenger.DoesNotExist:
        return render(request, "flights/error.html", {"message" : "No passenger."})

    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flight", args=(flight_id, )))
 
def login_view(request):
    try:
        username = request.POST["username"]
        password = request.POST["password"]
    except Exception:
        return render(request, "flights/login.html")
        

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "flights/login.html", {"message":"Invalid credentials."})


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        User.objects.create_user(username=username, password=password)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "flights/register.html");


def logout_view(request):
    logout(request)
    return render(request, "flights/home.html", {"message":None})

def home(request):
    return render(request, "flights/home.html")