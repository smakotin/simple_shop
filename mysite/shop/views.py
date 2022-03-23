from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
import requests
import json

from shop.forms import LoginForm
from shop.models import Product


class HomeShop(ListView):
    model = Product
    template_name = 'shop/index.html'


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            response = requests.post('http://127.0.0.1:8000/auth/token/login/', data={
                'username': username, 'password': password
            }
                                     )
            json_data = json.loads(response.text)
            token = json_data['auth_token']

            print(requests.get('http://127.0.0.1:8000/auth/users/me/', headers={'Authorization': f'Token {token}'}))

            return HttpResponseRedirect(redirect_to='http://127.0.0.1:8000/')

    else:
        form = LoginForm()

    return render(request, 'shop/login.html', {'form': form})
