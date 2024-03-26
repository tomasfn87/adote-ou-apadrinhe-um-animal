from django.core import validators
from django.core.files import File
from django.db import models
from django.utils import timezone as tz
import datetime as dt


class Animal(models.Model):
    def __str__(self):
        return "{} ({}/{}) incluído em: {}".format(
            self.nome,
            self.especie,
            self.sexo,
            self.adicionado_recentemente,
        )

    def adicionado_recentemente(self):
        now = tz.now()
        return now - dt.timedelta(days=1) <= self.adicionado_em <= now

    def validate_nome(value):
        if not any(char.isalpha() for char in value):
            raise validators.ValidationError(
                "O campo nome deve conter pelo menos uma letra.")

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
        blank=False,
        null=False,
    )

    SEXO_CHOICES = (
        ('m', 'macho'),
        ('f', 'fêmea'),
    )
    # sexo
    sexo = models.CharField(
        max_length=5,
        choices=SEXO_CHOICES,
        blank=False,
        null=False,
    )

    # imagem
    imagem = models.URLField(blank=False, null=False)

    # adicionado_em
    adicionado_em = models.DateTimeField(auto_now_add=True)

    # adicionado_por
    adicionado_por = models.CharField(max_length=100)


class Doacao(models.Model):
    def __str__(self):
        return f"{self.quantidade} {self.unidade} de {self.tipo_doacao} em {self.data_registro}"

    UNIDADE_CHOICES = (
        ('k', 'Kg'),
        ('g', 'Gramas'),
        ('u', 'Unidades'),
    )

    TIPO_DOACAO_CHOICES = (
        ('r', 'Racao'),
        ('a', 'Areia')
    )

    tipo_doacao   = models.CharField(max_length = 20)
    quantidade    = models.IntegerField()
    unidade       = models.CharField(max_length = 10, choices = UNIDADE_CHOICES)
    data_registro = models.DateTimeField()