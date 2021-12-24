from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('agency_create', views.agency_create, name='agency_create')
]
