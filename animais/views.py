from django.shortcuts import render
from django.views import generic

from .models import Animal

class IndexView(generic.ListView):
    template_name = "animais/index.html"
    context_object_name = "latest_animal_list"

    def get_queryset(self):
        """Retornar os últimos 5 animais cadastrados."""
        return Animal.objects.order_by("-adicionado_em")[:5]
