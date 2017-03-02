from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView, CreateView
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy
from .forms import ContactForm


class IndexView(TemplateView):
    template_name = 'index.html'


def contact(request):
    success = False
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.send_mail()
        success = True

    context = {
        'form': form,
        'success': success
    }
    return render(request, 'contact.html', context)


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    model = get_user_model()
    success_url = reverse_lazy('index')


index = IndexView.as_view()
register = RegisterView.as_view()
