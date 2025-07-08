from django import forms

from pets.models import Pets


class PetForm(forms.ModelForm):
    class Meta:
        model = Pets

        fields = ['name', 'date_of_birth', 'pet_img']

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'pet_img': forms.FileInput(attrs={
                'class': 'img_button',
                'id': 'id_pet_img',
            }),
        }
