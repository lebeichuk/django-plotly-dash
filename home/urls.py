from django.urls import path
from .views import Checkoutpage
from home.dash_apps.finished_apps import simpleexample


urlpatterns = [
    # path('', views.home, name='home'),
    path('checkout/', Checkoutpage.as_view(), name='checkout'),
]