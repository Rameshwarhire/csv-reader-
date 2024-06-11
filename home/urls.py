from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    # path('histogram',views.show_histo,name="histogram"),
    
]