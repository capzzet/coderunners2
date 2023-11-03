from django.urls import path
from .views import *
urlpatterns = [
    path('',index,name='home'),
    path('registration/',registration,name='registration'),
    path('success/',success,name='success'),
]
