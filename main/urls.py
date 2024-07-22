from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from main.views import NewsLetterDetailView, NewsLetterCreateView, NewsLetterUpdateView, NewsLetterDeleteView, \
    NewsLetterListView, ClientCreateView, ClientListView, ClientDetailView, ClientUpdateView, ClientDeleteView, \
    SendAttempListView
from main.apps import MainConfig

app_name = MainConfig.name

urlpatterns = [
    path('create/', NewsLetterCreateView.as_view(), name='newsletter_form'),
    path('<int:pk>/', NewsLetterDetailView.as_view(), name='newsletter_detail'),
    path('update/<int:pk>', never_cache(NewsLetterUpdateView.as_view()), name='newsletter_update'),
    path('delete/<int:pk>', NewsLetterDeleteView.as_view(), name='newsletter_delete'),
    path('', cache_page(60)(NewsLetterListView.as_view()), name='newsletter_list'),
    path('clients/create', ClientCreateView.as_view(), name='client_form'),
    path('clients/', cache_page(60)(ClientListView.as_view()), name='client_list'),
    path('clients/<int:pk>', ClientDetailView.as_view(), name='client_detail'),
    path('clients/update/<int:pk>', never_cache(ClientUpdateView.as_view()), name='client_update'),
    path('clients/delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
    path('sendattemps/', cache_page(60)(SendAttempListView.as_view()), name='sendattemp_list'),
]