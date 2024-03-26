from django import forms

from .models import Animal
from .models import Doacao


class AnimalForm(forms.ModelForm):
    arquivo_imagem = forms.FileField(
        label='Foto do animal',
        help_text='Formato Imagens recomendado: JPG; dimensões recomendadas: 1366 x 768 pixels.',
        required=True,
    )

    class Meta:
        model = Animal
        fields = ['nome', 'especie', 'sexo', 'arquivo_imagem']

    def save(self, commit=True):
        animal = super(AnimalForm, self).save(commit=False)
        if 'arquivo_imagem' in self.files:
            imagem = self.files['arquivo_imagem']
        if commit:
            animal.save()
        return animal