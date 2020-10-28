from django.urls import path
from . import views

urlpatterns=[
    path('', views.index, name='home'),
    path('delete/<company_name>/', views.delete_company, name='delete_company')
]