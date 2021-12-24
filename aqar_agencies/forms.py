from django import forms

class AgencyCreateForm(forms.Form):
    name = forms.CharField()
    phone_number = forms.CharField(required=False)
    profile_picture = forms.ImageField(required=False)
    email = forms.EmailField(required=False)
    address = forms.CharField(max_length=200, required=False)
    twitter = forms.CharField(max_length=50, required=False)
    instagram = forms.CharField(max_length=50, required=False)
