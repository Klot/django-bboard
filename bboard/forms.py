from django.conf import settings
from django.forms import ModelForm, DecimalField
from django import forms
from django.forms.widgets import Select

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import date

from .models import Bb, Rubric, Profile, Car, CarBrands, CarModels


class StartForm(ModelForm):
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(), label='Рубрика', help_text='Выберите рубрику.',
                                    widget=forms.widgets.Select(attrs={'size': 8}))

    class Meta:
        model = Rubric
        fields = ('rubric',)


class BbForm(ModelForm):
    price = forms.DecimalField(label='Цена', decimal_places=2)
    photo = forms.ImageField(label='Фото', required=False)

    class Meta:
        model = Bb
        fields = ('title', 'kind', 'photo', 'content', 'price')

    def clean_title(self):
        val = self.cleaned_data['title']
        if val == 'Человек':
            raise ValidationError('Работорговля запрещена!')
        return val


class CarBrandsForm(ModelForm):
    name = forms.ModelChoiceField(queryset=CarBrands.objects.all(), label='Марки', help_text='Выберите марку.',
                                  widget=forms.widgets.Select(attrs={'size': 8}))

    class Meta:
        model = CarBrands
        fields = ('name',)


class CarModelsForm(ModelForm):
    model = forms.ModelChoiceField(queryset=CarModels.objects.all(), label='Модель', help_text='Выберите модель.',
                                   widget=forms.widgets.Select(attrs={'size': 8}))

    class Meta:
        model = CarBrands
        fields = ('model',)


class CarForm(ModelForm):
    title = forms.CharField(label='Название авто')
    price = forms.DecimalField(label='Цена', decimal_places=2)
    photo = forms.ImageField(label='Фото', required=False)
    model = forms.ModelChoiceField(queryset=CarModels.objects.all(), label='Модель', help_text='Выберите модель.',
                                   widget=forms.widgets.Select(attrs={'size': 8}))

    class Meta:
        model = Car
        fields = ('title', 'kind', 'model', 'year', 'pts', 'owners', 'body', 'engine_type', 'drive', 'mileage',
                  'equip', 'status', 'color', 'photo', 'content', 'price')

    def clean_title(self):
        val = self.cleaned_data['title']
        if val == 'Человек':
            raise ValidationError('Работорговля запрещена!')
        return val

    def clean_year(self):
        val = self.cleaned_data['year']
        current_date = date.today()
        print(current_date)
        if (int(val) < int('1900')) or (int(val) > current_date.year):
            raise ValidationError('Дата выпуска введена неверно!')
        return val

    def __init__(self, carbrand_id, *args, **kwargs):
        super(CarForm, self).__init__(*args, **kwargs)
        self.fields['model'].queryset = CarModels.objects.filter(brand=carbrand_id)


class CarFormEdit(ModelForm):
    title = forms.CharField(label='Название авто')
    price = forms.DecimalField(label='Цена', decimal_places=2)
    photo = forms.ImageField(label='Фото', required=False)

    class Meta:
        model = Car
        fields = ('title', 'kind', 'model', 'year', 'pts', 'owners', 'body', 'engine_type', 'drive', 'mileage',
                  'equip', 'status', 'color', 'photo', 'content', 'price')

    def clean_title(self):
        val = self.cleaned_data['title']
        if val == 'Человек':
            raise ValidationError('Работорговля запрещена!')
        return val

    def clean_year(self):
        val = self.cleaned_data['year']
        current_date = date.today()
        print(current_date)
        if (int(val) < int('1900')) or (int(val) > current_date.year):
            raise ValidationError('Дата выпуска введена неверно!')
        return val


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(ModelForm):
    birth_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, label='День рождения')

    class Meta:
        model = Profile
        fields = ('phone_number', 'birth_date')
