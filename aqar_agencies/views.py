from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import AgencyCreateForm
from django.contrib.auth.models import User
from .models import Agency

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
    context = {'form': form}
    return render(request, "registration/register.html", context)

def agency_create(request):
    if request.method == 'POST':
        agency_form = AgencyCreateForm(request.POST, request.FILES)
        if agency_form.is_valid():
            agency_fields = agency_form.cleaned_data
            member = User.objects.get(username=request.user)
            Agency.objects.new(member,
                name=agency_fields['name'],
                phone_number=agency_fields['phone_number'],
                profile_picture=agency_fields['profile_picture'],
                email=agency_fields['email'],
                address=agency_fields['address'],
                twitter=agency_fields['twitter'],
                instagram=agency_fields['instagram'],
            )
            return redirect('index')
    agency_form = AgencyCreateForm()
    context = {'agency_form': agency_form}
    return render(request, "aqar_agencies/agency_create.html", context)

def agency_profile(request):
    pass