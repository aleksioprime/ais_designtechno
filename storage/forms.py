from django import forms
from employee.models import User
from storage.models import Thing, UseThings, Location, Equipment, CompositionEquipment, Status
from datetime import date

class ThingForm(forms.ModelForm):            
    name_manufacturer = forms.CharField(required=True, max_length=255, label='Название от производителя')
    manufacturer = forms.CharField(required=False, max_length=255, label='Производитель')
    name_bookkeeping = forms.CharField(required=False, max_length=255, label='Наименование от бухгалтерии')
    inventory_number = forms.CharField(required=False, max_length=16, label='Инвентарный номер')
    description = forms.CharField(widget=forms.Textarea, required=False, label='Описание')
    base_location = forms.ModelChoiceField(queryset=Location.objects.all(), required=False, label='Базовое местоположение')
    price = forms.DecimalField(widget=forms.TextInput, label='Цена', decimal_places=2, min_value=0, required=False)
    count = forms.DecimalField(widget=forms.NumberInput, required=True, label='Количество', decimal_places=0, min_value=1)
    finresp = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='teacher'), required=True, label='Ответственный пользователь')
    comment = forms.CharField(widget=forms.Textarea, required=False, label='Комментарии')
    photo = forms.ImageField(label='Фотография', required=False)
    photo_base_location = forms.ImageField(label='Фотография метонахождения', required=False)
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=False, label='Статус')
    url_site = forms.CharField(required=False, label='Ссылка на сайт')
    def __init__(self, *args, **kwargs):
        super(ThingForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
        self.fields['count'].widget.attrs['value'] = 1
        self.fields['finresp'].empty_label="Выберите ответственного"
        self.fields['base_location'].empty_label="Выберите кабинет"
        self.fields['status'].empty_label="Выберите статус"
    def save(self, *args, **kwargs):
        super(ThingForm, self).save(*args, **kwargs)
        return self
    class Meta:
        model = Thing
        fields = ['name_manufacturer', 'manufacturer', 'name_bookkeeping', 'inventory_number', \
            'description', 'base_location', 'base_location', 'price', 'count', 'photo', 'photo_base_location', 'finresp', 'url_site', 'status']

class UseThingsForm(forms.ModelForm):            
    thing = forms.ModelChoiceField(queryset=Thing.objects.all(), required=True, label='Позиция')
    employee = forms.ModelChoiceField(queryset=User.objects.all(), required=True, label='Сотрудник')
    count = forms.DecimalField(widget=forms.NumberInput, required=True, label='Количество', decimal_places=0, min_value=1)
    justification = forms.CharField(widget=forms.Textarea, required=False, label='Обоснование')
    location = forms.CharField(required=False, max_length=255, label='Местоположение')
    def __init__(self, *args, **kwargs):
        super(UseThingsForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
    def save(self, *args, **kwargs):
        super(UseThingsForm, self).save(*args, **kwargs)
        return self
    class Meta:
        model = UseThings
        fields = ['thing', 'employee', 'count', 'justification', 'location']


class EquipmentForm(forms.ModelForm):
    name = forms.CharField(required=False, max_length=255, label='Наименование')
    photo = forms.ImageField(label='Фотография', required=False)
    info = forms.CharField(widget=forms.Textarea, required=False, label='Информация')
    def __init__(self, *args, **kwargs):
        super(EquipmentForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
    def save(self, *args, **kwargs):
        super(EquipmentForm, self).save(*args, **kwargs)
        return self
    class Meta:
        model = Equipment
        fields = ['name', 'photo', 'info']

class ComposEquipmentForm(forms.ModelForm):  
    thing = forms.ModelChoiceField(queryset=Thing.objects.all(), required=True, label='Позиция')    
    equipment = forms.ModelChoiceField(queryset=Equipment.objects.all(), required=True, label='Элемент')    
    count = forms.DecimalField(widget=forms.NumberInput, required=True, label='Количество', decimal_places=0, min_value=1) 

    def __init__(self, *args, **kwargs):
        super(ComposEquipmentForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
        self.fields['count'].initial = 1
        self.fields['equipment'].empty_label="Выберите элемент"
        self.fields['thing'].widget.attrs.update({'style': 'display:none'})
    def save(self, *args, **kwargs):
        super(ComposEquipmentForm, self).save(*args, **kwargs)
        return self   
    class Meta:
        model = CompositionEquipment
        fields = ['thing', 'equipment', 'count']