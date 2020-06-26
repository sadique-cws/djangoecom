from django.urls import path,include
from store.views import *
app_name = "store"

urlpatterns = [
    path("",HomeView.as_view(),name="homepage")

]
