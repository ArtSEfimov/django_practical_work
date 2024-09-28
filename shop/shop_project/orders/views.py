from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from common.views import TitleMixin
from products.models import Basket

from .forms import OrderForm
from .models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ!'


class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'


class OrderListView(TitleMixin, ListView):
    model = Order
    template_name = 'orders/orders.html'
    title = 'Store - Заказы'
    ordering = ('-created',)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(TitleMixin, DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Store - Заказ #{self.object.id}'
        return context


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
            line_items=Basket.objects.filter(user=self.request.user).stripe_products(),
            mode='payment',
            metadata={'order_id': self.object.id},
            success_url=f"{settings.DOMAIN_NAME}{reverse('orders:order_success')}",
            cancel_url=f"{settings.DOMAIN_NAME}{reverse('orders:order_canceled')}",
        )

        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)


endpoint_secret = settings.STRIPE_SECRET


def fulfill_checkout(session_id):
    # Retrieve the Checkout Session from the API with line_items expanded
    checkout_session = stripe.checkout.Session.retrieve(
        session_id,
        expand=['line_items'],
    )

    order_id = int(checkout_session.metadata['order_id'])
    order = Order.objects.get(pk=order_id)
    order.update_after_payment()

    # Check the Checkout Session's payment_status property
    # to determine if fulfillment should be peformed
    if checkout_session.payment_status != 'unpaid':
        pass
        # TODO: Perform fulfillment of the line items

        # TODO: Record/save fulfillment status for this
        # Checkout Session


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if (
            event['type'] == 'checkout.session.completed'
            or event['type'] == 'checkout.session.async_payment_succeeded'
    ):
        fulfill_checkout(event['data']['object']['id'])

    return HttpResponse(status=200)
