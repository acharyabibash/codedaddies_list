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
    post_listings = soup.find_all('li', {'class': 'result-row'})
    # post_title = post_listings[0].find(class_= 'result-title').text
    # post_url = post_listings[0].find('a').get('href')
    # post_price = post_listings[0].find(class_= 'result-title').text
    # print(post_titles[0].get('href'))
    
    # print(post_title)
    # print(post_url)
    # print(post_price)

    # print(data)

    # print(search)

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        final_postings.append((post_title,post_url,post_price))

    stuff_for_frontend = {
        'search':search,
        'final_postings': final_postings,
    }
    return render(request,'my_app/new_search.html',stuff_for_frontend)
