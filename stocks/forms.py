from django.forms import ModelForm, TextInput, forms
from .models import Company

class CompanyForm(ModelForm):
    class Meta:
        model=Company
        fields=['name']
        widgets= {'name': TextInput(attrs={'class':'form-control form-control-lg form-control-borderless', 'placeholder':'Company Ticker Name' })}