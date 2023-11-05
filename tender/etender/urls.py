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
    path('personal/', personal, name='personal'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('tender/<int:tender_id>/', tender_detail, name='tender_detail'),

]
