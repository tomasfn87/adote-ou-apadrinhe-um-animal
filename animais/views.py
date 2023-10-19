from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.utils import timezone as tz

from .models import Animal
from .forms import AnimalForm

class IndexView(generic.ListView):
    template_name = "animais/index.html"
    context_object_name = "latest_animal_list"

    def get_queryset(self):
        """Retornar os últimos 5 animais cadastrados."""
        return Animal.objects.order_by("-adicionado_em")[:5]

def cadastro(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            form.save()
            # Redireciona para alguma página de sucesso ou outra página
            return HttpResponse('Página de sucesso')
    else:
        form = AnimalForm()
    return render(request, 'animais/cadastro.html', {'form': form})