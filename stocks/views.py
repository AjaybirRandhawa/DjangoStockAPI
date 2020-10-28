import requests
from django.shortcuts import render, redirect
from .models import Company
from .forms import CompanyForm
import yfinance as yf
import math
import urllib3

# Create your views here.
def fmt(n):

    millnames = ['',' T',' M',' B',' T']
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

def index(request):

    err_msg= ''
    message=''
    message_class=''

    if request.method == 'POST':
        form=CompanyForm(request.POST)
        if form.is_valid():
            new_company = form.cleaned_data['name']
            existing_Company_Count = Company.objects.filter(name=new_company).count()
            if existing_Company_Count == 0:
                r = yf.Ticker(str(new_company))
                try:
                    if r.info:
                        print(r.info)
                        form.save()
                except:
                    err_msg= 'Please enter the ticker symbol!'
            else:
                err_msg = 'Company already exists!'
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'Company added successfully!'
            message_class = 'is-success'
    form = CompanyForm()

    companies = Company.objects.all()
    stock_data=[]
    num=0
    for company in companies:
        current_company= yf.Ticker(str(company))
        print(str(company))
        new_num = num%1
        num+=1
        info_need= {
            'name': current_company.info['longName'],
            'symbol': str(company),
            'price': current_company.info['regularMarketPrice'],
            'sector': current_company.info['sector'],
            'website': current_company.info['website'],
            'previousClose': current_company.info['previousClose'],
            'marketOpen': current_company.info['regularMarketOpen'],
            'marketHigh': current_company.info['regularMarketDayHigh'],
            'marketLow': current_company.info['regularMarketDayLow'],
            'currency': current_company.info['currency'],
            'marketVolume': fmt(current_company.info['regularMarketVolume']),
            'num':new_num
        }
        stock_data.append(info_need)
    context = {'stock_data': stock_data, 
            'form' : form,
            'message': message,
            'message_class': message_class}
    return render(request, 'stocksapi/stocks.html', context)


def delete_company(request, company_name):
    Company.objects.get(name=company_name).delete()

    return redirect('home')