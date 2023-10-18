from django.db import models
from django.utils import timezone as tz
import datetime as dt

class Animal(models.Model):
    def __str__(self):
        return f"{self.nome} ({self.especie}/{self.sexo}) incluído em: {self.adicionado_em}"

    def adicionado_recentemente(self):
        now = tz.now()
        return now - dt.timedelta(days=1) <= self.adicionado_em <= now

    nome = models.CharField(max_length=500)

    ANIMAIS_CHOICES = (
        ('c', 'cachorro'),
        ('g', 'gato')
    )
    especie = models.CharField(
        max_length=8,
        choices=ANIMAIS_CHOICES,
    )

    SEXO_CHOICES = (
        ('m', 'macho'),
        ('f', 'fêmea')
    )
    sexo = models.CharField(
        max_length=5,
        choices=SEXO_CHOICES,
    )

    adicionado_em = models.DateTimeField("data de cadastro do animal")
