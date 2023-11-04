from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect

from etender.forms import TenderForm
from etender.models import *


# Create your views here.
navigation_links = [
    {'url': 'ads', 'title': 'Объявления'},
    {'url': 'registration', 'title': 'Планы'},
    {'url': 'registration', 'title': 'Аукционы'},
    {'url': 'registration', 'title': 'Контракты'},
]
registration_links = [
        {'url': '#', 'title': 'Вход'},
        {'url': '#', 'title': 'Зарегистрироваться'},
    ]
def index(request):

    clients1 = [
        {'image': 'etender/img/skyline.png', 'alt': 'Client 1', 'title': 'Коммерческие закупки', 'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'},
        {'image': 'etender/img/skyline.png', 'alt': 'Client 2', 'title': 'Коммерческие закупки', 'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'},
        {'image': 'etender/img/skyline.png', 'alt': 'Client 3', 'title': 'Коммерческие закупки', 'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'},
        {'image': 'etender/img/skyline.png', 'alt': 'Client 4', 'title': 'Коммерческие закупки', 'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'},
    ]
    auction_images = [
        {'url': 'etender/img/auc-icon.png', 'alt': 'Image 1', 'text': 'Регистрация на E-Tender'},
        {'url': 'etender/img/auc-icon.png', 'alt': 'Image 1', 'text': 'Регистрация на E-Tender'},
        {'url': 'etender/img/auc-icon.png', 'alt': 'Image 1', 'text': 'Регистрация на E-Tender'},
        {'url': 'etender/img/auc-icon2.png', 'alt': 'Image 2', 'text': 'Регистрация на E-Tender'},
        {'url': 'etender/img/auc-icon2.png', 'alt': 'Image 2', 'text': 'Регистрация на E-Tender'},
        {'url': 'etender/img/auc-icon2.png', 'alt': 'Image 2', 'text': 'Регистрация на E-Tender'},
    ]

    tender_services = [
        {'background_image': 'etender/img/1.jpg', 'title': 'КАК РАБОТАТЬ С БАЗОЙ ГОСУДАРСТВЕННЫХ ТЕНДЕРОВ'},
        {'background_image': 'etender/img/2.jpg', 'title': 'КАК РАБОТАТЬ С БАЗОЙ ГОСУДАРСТВЕННЫХ ТЕНДЕРОВ'},
        {'background_image': 'etender/img/3.jpg', 'title': 'КАК РАБОТАТЬ С БАЗОЙ ГОСУДАРСТВЕННЫХ ТЕНДЕРОВ'},
        {'background_image': 'etender/img/4.jpg', 'title': 'КАК РАБОТАТЬ С БАЗОЙ ГОСУДАРСТВЕННЫХ ТЕНДЕРОВ'},
    ]
    useful_links = [
        {'url': '#', 'title': 'Министерство финансов Кыргызской Республики'},
        {'url': '#', 'title': 'Центральное казначейство МФ КР'},
        {'url': '#', 'title': 'Государственное агентство антимонопольного регулирования при ПКР'},
        {'url': '#', 'title': 'Министерство финансов Кыргызской Республики'},
        {'url': '#', 'title': 'Министерство финансов Кыргызской Республики'},
    ]

    links_buttons = [
        {'url': '#', 'title': 'Реестр'},
        {'url': '#', 'title': 'Документы'},
        {'url': '#', 'title': 'Справочники'},
        {'url': '#', 'title': 'Помощь'},
        {'url': '#', 'title': 'Жалобы'},
    ]

    clients = [
        {'image': 'etender/img/alfa.png', 'alt': 'Client 1'},
        {'image': 'etender/img/alfa.png', 'alt': 'Client 2'},
        {'image': 'etender/img/alfa.png', 'alt': 'Client 3'},
        {'image': 'etender/img/alfa.png', 'alt': 'Client 4'},
        {'image': 'etender/img/IUK.png', 'alt': 'Client 5'},
        {'image': 'etender/img/IUK.png', 'alt': 'Client 6'},
        {'image': 'etender/img/IUK.png', 'alt': 'Client 7'},
        {'image': 'etender/img/IUK.png', 'alt': 'Client 8'},
    ]

    context = {
        'navigation_links': navigation_links,
        'registration_links': registration_links,
        'clients1': clients1,
        'auction_images': auction_images,
        'tender_services': tender_services,
        'useful_links': useful_links,
        'links_buttons': links_buttons,
        'clients': clients,
        'user': request.user,
    }

    return render(request, 'etender/html/index.html', context)


from django.contrib.auth import authenticate, login


def registration(request):
    if request.method == 'POST':
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        middle_name = request.POST.get('middle_name', '')
        password = request.POST['password']
        phone_number = request.POST['phone_number']
        email = request.POST['email']

        user = User.objects.create_user(username=email, password=password, email=email, first_name=first_name, last_name=last_name)
        user_profile = UserProfile(
            user=user,
            phone_number=phone_number,
        )
        user_profile.save()

        login(request, user)

        return redirect('success')

    return render(request, 'etender/html/registration.html')
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('success')
        else:
            error_message = "Неверные учетные данные. Пожалуйста, попробуйте снова."
            return render(request, 'etender/html/login.html', {'error_message': error_message})

    if request.user.is_authenticated:
        return redirect('success')

    return render(request, 'etender/html/login.html')
def logout_view(request):
    logout(request)
    return redirect('home')


def success(request):
    return render(request, 'etender/html/success.html')

def ads(request):
    tenders = Tender.objects.all()

    if request.method == 'POST':
        form = TenderForm(request.POST)
        if form.is_valid():

            Tender.objects.create(
                purchase_name=form.cleaned_data['purchase_name'],
                purchase_method=form.cleaned_data['purchase_method'],
                purchase_number=form.cleaned_data['purchase_number'],
                purchase_type=form.cleaned_data['purchase_type'],
                organization_name=form.cleaned_data['organization_name'],
                planned_amount=form.cleaned_data['planned_amount'],
                publication_date=form.cleaned_data['publication_date'],
                proposal_deadline=form.cleaned_data['proposal_deadline']
            )

            return redirect('ads')

    else:
        form = TenderForm()

    context = {
        'navigation_links': navigation_links,
        'registration_links': registration_links,
        'tenders': tenders,
        'form': form
    }
    return render(request, 'etender/html/ads.html', context)

@login_required
def add_tender(request):
    if request.method == 'POST':
        form = TenderForm(request.POST)
        if form.is_valid():
            tender = Tender(
                purchase_name=form.cleaned_data['purchase_name'],
                purchase_method=form.cleaned_data['purchase_method'],
                purchase_number=form.cleaned_data['purchase_number'],
                purchase_type=form.cleaned_data['purchase_type'],
                organization_name=form.cleaned_data['organization_name'],
                planned_amount=form.cleaned_data['planned_amount'],
                publication_date=form.cleaned_data['publication_date'],
                proposal_deadline=form.cleaned_data['proposal_deadline']
            )
            tender.save()
            return redirect('ads')
    else:
        form = TenderForm()

    context = {
        'form': form,
        'navigation_links': navigation_links,
        'registration_links': registration_links,
    }
    return render(request, 'etender/html/add_tender.html', context)