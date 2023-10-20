from django.core import validators
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone as tz

import datetime as dt

class Animal(models.Model):
    def __str__(self):
        return f"{self.nome} ({self.especie}/{self.sexo}) incluído em: {self.adicionado_em}"

    def adicionado_recentemente(self):
        now = tz.now()
        return now - dt.timedelta(days=1) <= self.adicionado_em <= now

    def validate_nome(value):
        if not any(char.isalpha() for char in value):
            raise validators.ValidationError("O campo nome deve conter pelo menos uma letra.")

    # nome
    nome = models.CharField(
        max_length=100,
        validators=[validate_nome],
        blank=False,
        null=False,
    )

    ESPECIE_CHOICES = (
        ('c', 'cachorro'),
        ('g', 'gato'),
        ('o', 'outro'),
    )
    # especie
    especie = models.CharField(
        max_length=8,
        verbose_name='espécie',
        choices=ESPECIE_CHOICES,
    )

    SEXO_CHOICES = (
        ('m', 'macho'),
        ('f', 'fêmea'),
    )
    # sexo
    sexo = models.CharField(
        max_length=5,
        choices=SEXO_CHOICES,
    )

    # adicionado_em
    adicionado_em = models.DateTimeField(auto_now_add=True)
