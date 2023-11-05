from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from etender.forms import TenderForm
from etender.models import *
from django_filters import rest_framework as filters

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
        {'image': 'etender/img/section-1.png', 'alt': 'Client 1', 'title': 'Государственные закупки', 'text': 'Приобретение товаров и услуг государством для обеспечения прозрачности и эффективного использования бюджетных средств.'},
        {'image': 'etender/img/section-3.png', 'alt': 'Client 2', 'title': 'Коммерческие закупки', 'text': 'Покупка товаров и услуг компаниями для удовлетворения своих потребностей и целей.'},
        {'image': 'etender/img/section-4.png', 'alt': 'Client 3', 'title': 'Аукцион', 'text': 'Способ продажи, при котором участники предлагают цены в конкурентной борьбе за товар или услугу.'},
        {'image': 'etender/img/section-2.png', 'alt': 'Client 4', 'title': 'Продажа и Аренда имущества', 'text': 'Данные о сделках, включая объекты, стороны, условия и результаты сделок с недвижимостью и движимостью.'},
    ]
    auction_images = [
        {'url': 'etender/img/auc-icon.png', 'alt': 'Image 1', 'text': 'Регистрация на E-Tender'},
        {'url': 'etender/img/auc-icon.png', 'alt': 'Image 1', 'text': 'Объявление аукциона'},
        {'url': 'etender/img/auc-icon.png', 'alt': 'Image 1', 'text': 'Регистрация заявки'},
        {'url': 'etender/img/auc-icon2.png', 'alt': 'Image 2', 'text': 'Проведение закупок'},
        {'url': 'etender/img/auc-icon2.png', 'alt': 'Image 2', 'text': 'Подписание протокола'},
        {'url': 'etender/img/auc-icon2.png', 'alt': 'Image 2', 'text': 'Заключение договора'},
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
        {'url': '#', 'title': 'Торгово-промышленная палата Кыргызской Республики'},
    ]

    links_buttons = [
        {'url': '#', 'title': 'Реестр'},
        {'url': '#', 'title': 'Документы'},
        {'url': '#', 'title': 'Справочники'},
        {'url': '#', 'title': 'Помощь'},
        {'url': '#', 'title': 'Жалобы'},
    ]

    clients = [
        {'image': 'etender/img/logo/alfa.png', 'alt': 'Client 1'},
        {'image': 'etender/img/logo/alfa.png', 'alt': 'Client 2'},
        {'image': 'etender/img/logo/alfa.png', 'alt': 'Client 3'},
        {'image': 'etender/img/logo/alfa.png', 'alt': 'Client 4'},
        {'image': 'etender/img/logo/IUK.png', 'alt': 'Client 5'},
        {'image': 'etender/img/logo/IUK.png', 'alt': 'Client 6'},
        {'image': 'etender/img/logo/IUK.png', 'alt': 'Client 7'},
        {'image': 'etender/img/logo/IUK.png', 'alt': 'Client 8'},
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



class TenderFilter(filters.FilterSet):
    class Meta:
        model = Tender
        fields = {
            'planned_amount': ['exact', 'lt', 'gt'],
            'publication_date': ['exact', 'lt', 'gt'],
        }

def ads(request):
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort_by')
    sort_direction = request.GET.get('sort_direction', 'asc')
    items_per_page = request.GET.get('items_per_page', 3)

    tenders = Tender.objects.annotate(
        sorted_planned_amount=F('planned_amount')
    )

    if search_query:
        tenders = tenders.filter(
            Q(purchase_name__icontains=search_query) |
            Q(purchase_method__icontains=search_query) |
            Q(organization_name__icontains=search_query)
        )

    if sort_direction == 'desc':
        sort_by = f'-{sort_by}' if sort_by else '-planned_amount'
    else:
        sort_by = sort_by if sort_by else 'planned_amount'

    tenders = tenders.order_by(sort_by)

    paginator = Paginator(tenders, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        form = TenderForm(request.POST)
        if form.is_valid():
            Tender.objects.create(**form.cleaned_data)
            return redirect('ads')
    else:
        form = TenderForm()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        tender_list_html = render_to_string('etender/html/tender_list.html', {'tenders': page_obj})
        return JsonResponse({'tender_list_html': tender_list_html})

    context = {
        'navigation_links': navigation_links,
        'registration_links': registration_links,
        'tenders': page_obj,
        'form': form,
        'search_query': search_query
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
            tender.user = request.user
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


@login_required
def tender_detail(request, tender_id):
    tender = get_object_or_404(Tender, id=tender_id)
    if request.method == 'POST' and 'edit_tender' in request.POST:
        if request.user == tender.user:
            return redirect('tender_detail', tender_id=tender.id)
        else:
            return HttpResponse("У вас нет прав на редактирование этого тендера.")

    elif request.method == 'POST' and 'delete_tender' in request.POST:
        if request.user == tender.user:
            return redirect('ads')
        else:
            return HttpResponse("У вас нет прав на удаление этого тендера.")

    else:
        context = {
            'navigation_links': navigation_links,
            'registration_links': registration_links,
            'tender': tender,
        }
        return render(request, 'etender/html/tender_detail.html', context)

def edit_tender(request, tender_id):
    if request.method == 'GET' and request.is_ajax():
        try:
            tender = Tender.objects.get(pk=tender_id)
            tender.purchase_name = 'Новое название'
            tender.save()
            return JsonResponse({'success': True, 'tender': {'purchase_name': tender.purchase_name}})
        except Tender.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Тендер не найден'})
    else:
        return JsonResponse({'success': False, 'error': 'Неправильный запрос'})

def delete_tender(request, tender_id):
    if request.method == 'POST' and request.is_ajax():
        tender = get_object_or_404(Tender, pk=tender_id, user=request.user)
        tender.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Неправильный запрос'})
@receiver(pre_save, sender=Tender)
def assign_user(sender, instance, **kwargs):
    if not instance.user:
        instance.user = User.objects.get(username='root')
def personal(request):
    user_tenders = Tender.objects.filter(user=request.user)
    context = {
        'navigation_links': navigation_links,
        'registration_links': registration_links,
        'user_tenders': user_tenders
    }
    return render(request, 'etender/html/personal.html', context)
def edit_profile(request):
    return HttpResponse('edit')