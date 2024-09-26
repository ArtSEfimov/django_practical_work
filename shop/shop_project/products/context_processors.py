def baskets(request):
    from .models import Basket
    context_dict = {'baskets': None}
    user = request.user
    if user.is_authenticated:
        context_dict.update(
            {'baskets': Basket.objects.filter(user=user)}
        )

    return context_dict
