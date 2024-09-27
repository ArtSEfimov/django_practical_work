from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView
from django.conf import settings
from common.views import TitleMixin
from .forms import OrderForm
import stripe
from django.http import HttpResponseRedirect
from http import HTTPStatus

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ!'


class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Store - Оформление заказа'

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        super().post(self, request, *args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1Q3m5O02Kvz3MzXl8E05bLMr',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f"{settings.DOMAIN_NAME}{reverse('orders:order_success')}",
            cancel_url=f"{settings.DOMAIN_NAME}{reverse('orders:order_canceled')}",
        )

        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)
