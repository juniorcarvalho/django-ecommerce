from django.shortcuts import render
from .forms import ContactForm
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

index = IndexView.as_view()


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

