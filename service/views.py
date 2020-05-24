from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import View
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile

from datetime import datetime

from service.forms import CreateOrderForm

from .models import Order, Photo


class ServicePage(View):
    def get(self, request):
        form = CreateOrderForm()
        return render(request, 'service/index.html', context={'form': form})

    def post(self, request):
        form = CreateOrderForm(request.POST, request.FILES)

        if form.is_valid():
            cd = form.cleaned_data
            order = Order.objects.create(last_name=cd['last_name'],
                                         first_name=cd['first_name'],
                                         tel=cd['tel'],
                                         size=cd['size'],
                                         quantity=cd['quantity'],
                                         comment=cd['comment'],
                                         total_price=cd['total_price'],
                                         accept_conditions=cd['accept_conditions'])
            for f in request.FILES.getlist('photos'):
                data = f.read()
                date = datetime.now()
                photo = Photo(order=order)
                photo.photos.save(f'{date.minute}{date.second}.{f.name.split(".")[-1]}', ContentFile(data))
                photo.save()
            subject = f'{cd["tel"]} | {cd["last_name"]} | {cd["size"]} x {cd["quantity"]} = {cd["total_price"]}р. '
            message = f'{cd["tel"]} \n {cd["last_name"]} \n {cd["first_name"]} \n {cd["size"]} x {cd["quantity"]} = {cd["total_price"]}р. \n {cd["comment"]} '
            send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=['dpmbg@yandex.ru', 'pmbg@yandex.ru'])
            messages.success(request, f'Ваш заказ успешно зарегистрирован! '
                                      f'Для оплаты заказа вам необходимо пополнить кошелек ЯндексДеньги на сумму в размере - {cd["total_price"]} руб. ')
            return redirect('ServicePage')
        return HttpResponse('Error')

