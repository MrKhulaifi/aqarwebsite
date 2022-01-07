from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import AgencyCreateForm, AgencyChoiceForm
from django.contrib.auth.models import User
from .models import Agency, AgencyMember

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

def agency_choice(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        agency_memberships = AgencyMember.objects.filter(member=user)
        if len(agency_memberships) == 1 :
            return redirect("agency_profile")
        
        form = AgencyChoiceForm(agency_memberships=agency_memberships)
        context = {
            "agency_memberships": agency_memberships,
            "number_of_memberships": len(agency_memberships),
            "form": form
        }
        return render(request, 'aqar_agencies/agency_choice.html', context)
    else:
        return render(request, 'aqar_agencies/agency_choice.html')

def agency_profile(request):
    if request.user.is_authenticated:
        # user = User.objects.get(username=request.user)
        if request.method == "POST":
            print(request.POST["agency"], "HEEEEEERE")
            agency_form = AgencyChoiceForm(request.POST)
            if agency_form.is_valid():
                agency = agency_form.cleaned_data['agency']
                print(agency)
        context = {
            'name': agency.name
        }
        return render(request, 'aqar_agencies/agency_profile.html', context)
    else:
        return render(request, 'aqar_agencies/agency_profile.html')

# --------------------------------------------------------------------------------------

def learning_view(request):
    pass