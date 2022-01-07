from django import forms
from django.forms.fields import ChoiceField, MultipleChoiceField
from .models import Agency, AgencyMember

class AgencyCreateForm(forms.Form):
    name = forms.CharField()
    phone_number = forms.CharField(required=False)
    profile_picture = forms.ImageField(required=False)
    email = forms.EmailField(required=False)
    address = forms.CharField(max_length=200, required=False)
    twitter = forms.CharField(max_length=50, required=False)
    instagram = forms.CharField(max_length=50, required=False)

class AgencyChoiceForm(forms.Form):
    agency = forms.ModelChoiceField(queryset=AgencyMember.objects.none(), required=True, label= "Agency Choice")

    def __init__(self, *args, **kwargs):
        agency_memberships = kwargs.pop("agency_memberships", None)
        super(AgencyChoiceForm, self).__init__()

        if agency_memberships:
            self.fields["agency"].queryset = agency_memberships
        