import random
from datetime import datetime, timedelta
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from manager.models import Card
from django.contrib import messages


def display(request):
    cards = Card.objects.all()

    search = request.GET.get("search")

    if search:
        cards = cards.filter(Q(series__icontains=search) | Q(number__icontains=search) | Q(release_date__icontains=search)
            | Q(expiration_date__icontains=search) | Q(status__icontains=search))

    return render(request, 'manager/home.html', {'cards':cards})

def card_info(request, card_pk):
    card = Card.objects.get(pk=card_pk)

    if request.method == 'POST':
        act_action = request.POST.get('activation')
        del_action = request.POST.get('delete')
        if act_action:
            card.status = request.POST.get('activation')
            card.save(update_fields=['status'])
        elif del_action:
            card.delete()
            messages.success(request, 'Карта успешно удалена!')
            return HttpResponseRedirect(reverse('display'))

    return render(request, 'manager/card.html', {'card':card})

def generator(request):

    #generates random date in given range
    def get_random_date(start, end):
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        return start + timedelta(seconds=random_second)

    if request.method == 'POST':
        if request.POST.get('series') and request.POST.get('quantity'):
            series = int(request.POST.get('series'))
            quantity = int(request.POST.get('quantity'))
            if 0 < quantity <= 100 and series > 0:
                for x in range(quantity):
                    card = Card()
                    card.series = series
                    rand_number = ''
                    for num in range(16):
                        rand_number += random.choice(['0','1','2','3','4','5','6','7','8','9'])
                    card.number = int(rand_number)

                    start_rel_dt = datetime.strptime('01.01.2020 00.00.00', '%d.%m.%Y %H.%M.%S')
                    end_rel_dt = datetime.now()
                    card.release_date = get_random_date(start_rel_dt, end_rel_dt)
                    days = int(request.POST.get('exp_date', 365)) #gets information of duration from the form
                    card.expiration_date = card.release_date + timedelta(days = days)

                    card.usage_date = datetime.now()

                    card.amount = random.random()*300000

                    if card.expiration_date < datetime.now():
                        card.status = 'Просрочена'
                    else:
                        card.status = random.choice(['Активирована', 'Не активирована'])
                    card.save()
                    messages.success(request, 'Карты успешно сгенерированы!')
            else:
                return render(request, 'manager/generator.html',
                              {'error':'Серия и количество должно быть положительным. Количество не должно превышать 100'})
        else:
            return render(request, 'manager/generator.html', {'error': 'Введите данные'})

    return render(request, 'manager/generator.html')