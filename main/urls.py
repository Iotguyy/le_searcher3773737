# main/urls.py

# from django.urls import path
# from .views import *
#
# urlpatterns = [
#     path('', home, name='home'),  # Define your URL patterns here
#     path('add/',add_name,name='add'),
#     path('fuzzy_search/',fuzzy_search,name='fuzzy'),
#     path('phonetic_search',phonetic_search,name='phonetic_search')
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_record, name='add_record'),
]