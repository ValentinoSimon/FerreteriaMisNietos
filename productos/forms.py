from django import forms

class SubirArchivos_fenix(forms.Form):
    file = forms.FileField()


class SubirArchivos_palomar(forms.Form):
    file = forms.FileField()


class SubirArchivos_electrimat(forms.Form):
    file = forms.FileField()