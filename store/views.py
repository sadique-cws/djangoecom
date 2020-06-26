from django.shortcuts import render
from store.models import *
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,DeleteView,UpdateView

class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home.html"


