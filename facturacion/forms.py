from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from .models import Cliente, Medicion, Boleta, Aviso
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
import re


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'direccion', 'email', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '200'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': '500'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'maxlength': '254'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20'}),
        }
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            # Sanitizar entrada
            nombre = strip_tags(nombre).strip()
            if len(nombre) < 2:
                raise ValidationError('El nombre debe tener al menos 2 caracteres.')
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
                raise ValidationError('El nombre solo puede contener letras y espacios.')
        return nombre
    
    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')
        if direccion:
            # Sanitizar entrada
            direccion = strip_tags(direccion).strip()
            if len(direccion) < 10:
                raise ValidationError('La dirección debe tener al menos 10 caracteres.')
        return direccion
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            # Sanitizar entrada
            telefono = strip_tags(telefono).strip()
            # Validar formato de teléfono
            if not re.match(r'^[\+]?[0-9\s\-\(\)]{8,20}$', telefono):
                raise ValidationError('Formato de teléfono inválido.')
        return telefono

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('telefono', css_class='form-group col-md-6 mb-3'),
            ),
            'direccion',
            Submit('submit', 'Guardar Cliente', css_class='btn btn-primary')
        )


class MedicionForm(forms.ModelForm):
    class Meta:
        model = Medicion
        fields = ['cliente', 'fecha', 'lectura_anterior', 'lectura_actual', 'observaciones']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lectura_anterior': forms.NumberInput(attrs={'class': 'form-control'}),
            'lectura_actual': forms.NumberInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('cliente', css_class='form-group col-md-6 mb-3'),
                Column('fecha', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('lectura_anterior', css_class='form-group col-md-6 mb-3'),
                Column('lectura_actual', css_class='form-group col-md-6 mb-3'),
            ),
            'observaciones',
            Submit('submit', 'Registrar Medición', css_class='btn btn-primary')
        )

    def clean(self):
        cleaned_data = super().clean()
        lectura_anterior = cleaned_data.get('lectura_anterior')
        lectura_actual = cleaned_data.get('lectura_actual')

        if lectura_anterior and lectura_actual:
            if lectura_actual < lectura_anterior:
                raise forms.ValidationError("La lectura actual no puede ser menor que la lectura anterior.")
            
            # Calcular consumo automáticamente
            consumo = lectura_actual - lectura_anterior
            cleaned_data['consumo_m3'] = consumo

        return cleaned_data


class BoletaForm(forms.ModelForm):
    class Meta:
        model = Boleta
        fields = ['cliente', 'medicion', 'fecha_vencimiento']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'medicion': forms.Select(attrs={'class': 'form-control'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('cliente', css_class='form-group col-md-6 mb-3'),
                Column('medicion', css_class='form-group col-md-6 mb-3'),
            ),
            'fecha_vencimiento',
            Submit('submit', 'Generar Boleta', css_class='btn btn-success')
        )


class AvisoForm(forms.ModelForm):
    class Meta:
        model = Aviso
        fields = ['cliente', 'tipo_aviso', 'titulo', 'mensaje']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'tipo_aviso': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('cliente', css_class='form-group col-md-6 mb-3'),
                Column('tipo_aviso', css_class='form-group col-md-6 mb-3'),
            ),
            'titulo',
            'mensaje',
            Submit('submit', 'Crear Aviso', css_class='btn btn-warning')
        )
