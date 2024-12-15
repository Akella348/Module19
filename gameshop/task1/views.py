from django.shortcuts import render
from .forms import UserRegister
from .models import Buyer, Game
from django.core.paginator import Paginator
from .models import News


def games_view(request):
    title = "Магазин"
    title2 = "Игры"
    comeback = "Вернуться обратно"
    games = Game.objects.all()  #  Получение списка игр из БД
    context = {
        'title': title,
        'title2': title2,
        'games': games,
        'comeback': comeback
    }
    return render(request, 'first_task/games.html', context)


def sign_up_by_django(request):
    info = {}
    form = UserRegister()

    if request.method == 'POST':
        form = UserRegister(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            existing_user = Buyer.objects.filter(name=username).exists()  # поиск пользователя с таким же username в БД

            if existing_user:
                info['error'] = 'Пользователь уже существует'
            elif password != repeat_password:
                info['error'] = 'Пароли не совпадают'
            elif age < 18:
                info['error'] = 'Вы должны быть старше 18'
            else:
                new_user = Buyer.objects.create(name=username, balance=0, age=age)  # добавление пользователя в БД
                return render(request, 'first_task/registration_page.html',
                              {'message': f'Приветствуем, {username}!'})
    info['form'] = form
    return render(request, 'first_task/registration_page.html', info)


def news_view(request):
    news_list = News.objects.all().order_by('-date')  # Сортируем по дате
    paginator = Paginator(news_list, 10)  # 10 новостей на странице

    page_number = request.GET.get('page')  # Получаем номер страницы
    page_obj = paginator.get_page(page_number)  # Получаем объекты для текущей страницы

    context = {
        'news': page_obj,
    }

    return render(request, 'first_task/news.html', context)


#  Убрал регистрацию по html
# def sign_up_by_html(request):
#     info = {}
#
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         repeat_password = request.POST.get('repeat_password')
#         age = int(request.POST.get('age', 0))
#
#         if username in users:  # Проверки на валидность
#             info['error'] = 'Пользователь уже существует'
#         elif password != repeat_password:
#             info['error'] = 'Пароли не совпадают'
#         elif age < 18:
#             info['error'] = 'Вы должны быть старше 18'
#         else:
#             info['message'] = f'Приветствуем, {username}!'
#
#             return render(request, 'fifth_task/registration_page.html', info)
#
#     return render(request, 'fifth_task/registration_page.html', info)