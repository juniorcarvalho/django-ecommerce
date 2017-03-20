from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView, TemplateView
from django.contrib import messages
from django.forms import modelformset_factory
from django.core.urlresolvers import reverse
from .models import CartItem
from ecommerce.catalog.models import Product


class CreateCartItemView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        if self.request.session.session_key is None:
            self.request.session.save()
        cart_item, created = CartItem.objects.add_item(self.request.session.session_key,
                                                       product)
        if created:
            messages.success(self.request, 'Produto adicionado ao carrinho.')
        else:
            messages.success(self.request, 'Produto atualizado ao carrinho.')
        return reverse('checkout:cart_item')


class CartItemView(TemplateView):
    template_name = 'checkout/cart.html'

    def get_formset(self):
        CartItemFormSet = modelformset_factory(
            CartItem, fields=('quantity',), can_delete=True, extra=0
        )
        session_key = self.request.session.session_key
        if session_key:
            formset = CartItemFormSet(
                queryset=CartItem.objects.filter(cart_key=session_key),
                                                 data=self.request.POST or None
            )
        else:
            formset = CartItemFormSet(
                queryset=CartItem.objects.none(), data=self.request.POST or None
            )
        return formset

    def get_context_data(self, **kwargs):
        context = super(CartItemView, self).get_context_data(**kwargs)
        context['formset'] = self.get_formset()

    def post(self, request, *args, **kwargs):
        formset = self.get_formset()
        if formset.is_valid():
            messages.success(request, 'Carrinho atualizado.')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


create_cartitem = CreateCartItemView.as_view()
cart_item = CartItemView.as_view()
