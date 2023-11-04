from django.urls import path
from .views import *
urlpatterns = [
    path('',index,name='home'),
    path('registration/',registration,name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('success/',success,name='success'),
    path('ads/',ads,name='ads'),
    path('add_tender/', add_tender, name='add_tender'),
]
