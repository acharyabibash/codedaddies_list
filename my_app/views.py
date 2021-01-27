import requests

from requests.compat import quote_plus 

from . import models

from django.shortcuts import render

from bs4 import BeautifulSoup


BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'

# Create your views here.
def home(request):
    return render(request,'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    # print(quote_plus(search))
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data,features = 'html.parser')
    post_titles = soup.find_all('a',{'class':'result-title'})
    print(post_titles[0].text)
    # print(data)
    # print(search)
    stuff_for_frontend = {
        'search':search,
    }
    return render(request,'my_app/new_search.html',stuff_for_frontend)
