from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import AgencyForm

def index(request):
    return render(request, 'aqar_agencies/index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    context = {"form": form}
    return render(request, "registration/register.html", context)

def create_agency(request):
    if request.method == 'POST':
        agency_form = AgencyForm(request.POST, request.FILES)

        if agency_form.is_valid():
            agency_form.save(commit=False)
        return redirect('index')
    agency_form = AgencyForm()
    context = {"agency_form": agency_form}
    return render(request, "aqar_agencies/create_agency.html", context)
