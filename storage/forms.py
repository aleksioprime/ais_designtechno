from django import forms
from employee.models import User
from storage.models import Thing, UseThing, Composition, Cabinet, Location, Status, StatusThing
from datetime import date

class ThingForm(forms.ModelForm):            
    name = forms.CharField(required=True, max_length=255, label='Название')
    is_accounting = forms.CheckboxInput()
    name_docs = forms.CharField(required=False, max_length=255, label='Наименование по документам')
    inventory = forms.CharField(required=False, max_length=255, label='Инвентарный номер')
    manufacturer = forms.CharField(required=False, max_length=255, label='Производитель')
    site = forms.CharField(required=False, label='Ссылка на сайт')
    is_material = forms.CheckboxInput()
    is_set = forms.CheckboxInput()
    description = forms.CharField(widget=forms.Textarea, required=False, label='Описание')
    comment = forms.CharField(widget=forms.Textarea, required=False, label='Комментарии')
    price = forms.DecimalField(widget=forms.TextInput, label='Цена', decimal_places=2, min_value=0, required=False)
    count = forms.DecimalField(widget=forms.NumberInput, required=True, label='Количество', decimal_places=0, min_value=1)
    picture = forms.ImageField(label='Изображение', required=False)
    photo = forms.ImageField(label='Фотография', required=False)
    person = forms.ModelChoiceField(User.objects.filter(groups__name='teacher').all(), required=False, label='Ответственное лицо')
    location_cabinet = forms.ModelChoiceField(queryset=Cabinet.objects.all(), required=True, label='Кабинет')
    location_name = forms.CharField(required=True, max_length=255, label='Конкретное описание')
    location_photo = forms.ImageField(label='Фотография', required=False)

    def __init__(self, *args, **kwargs):
        super(ThingForm, self).__init__(*args, **kwargs)
        self.fields['location'].widget.attrs.update({'style': 'display:none'})
        for field in iter(self.fields):
            if field not in ['is_accounting', 'is_set', 'is_material']:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                })
        self.fields['person'].empty_label="Ответственный сотрудник"
        self.fields['count'].widget.attrs['value'] = 1
        self.fields['location_cabinet'].empty_label="Выберите кабинет"
        self.fields['location'].widget.attrs.update({'style': 'display:none'})
    def save(self, *args, **kwargs):
        super(ThingForm, self).save(*args, **kwargs)
        return self
    class Meta:
        model = Thing
        fields = '__all__'
        exclude = ('employees', 'composition', 'statuses')

class UseThingForm(forms.ModelForm):            
    thing = forms.ModelChoiceField(queryset=Thing.objects.all(), required=True, label='Позиция')
    employee = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='teacher').all(), required=True, label='Сотрудник')
    count = forms.DecimalField(widget=forms.NumberInput, required=True, label='Количество', decimal_places=0, min_value=1)
    justification = forms.CharField(widget=forms.Textarea, required=False, label='Обоснование')
    location_cabinet = forms.ModelChoiceField(queryset=Cabinet.objects.all(), required=False, label='Кабинет')
    location_name = forms.CharField(required=True, max_length=255, label='Конкретное описание')
    location_photo = forms.ImageField(label='Фотография', required=False)

    def __init__(self, *args, **kwargs):
        super(UseThingForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
            self.fields[field].initial = ""
        self.fields['employee'].empty_label="Выберите сотрудника"
        self.fields['location_cabinet'].empty_label="Выберите кабинет"
        self.fields['location'].widget.attrs.update({'style': 'display:none'})
        self.fields['count'].initial = 1 
    def save(self, *args, **kwargs):
        super(UseThingForm, self).save(*args, **kwargs)
        return self
    class Meta:
        model = UseThing
        fields = '__all__'
        exclude = ('created', 'updated')


class CompositionForm(forms.ModelForm):
    thing = forms.ModelChoiceField(queryset=Thing.objects.all(), required=True, label='Позиция')
    equipment = forms.ModelChoiceField(queryset=Thing.objects.all(), required=True, label='Элемент')
    count = forms.DecimalField(widget=forms.NumberInput, required=True, label='Количество', decimal_places=0, min_value=1)
    def __init__(self, *args, **kwargs):
        super(CompositionForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
        self.fields['count'].initial = 1
        self.fields['equipment'].empty_label="Выберите элемент"
        self.fields['thing'].widget.attrs.update({'style': 'display:none'})
    def save(self, *args, **kwargs):
        super(CompositionForm, self).save(*args, **kwargs)
        return self
    class Meta:
        model = Composition
        fields = ['thing', 'equipment', 'count']

class StatusThingForm(forms.ModelForm):
    thing = forms.ModelChoiceField(queryset=Thing.objects.all(), required=True, label='Позиция')
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=True, label='Статус')
    count = forms.DecimalField(widget=forms.NumberInput, required=True, label='Количество', decimal_places=0, min_value=1)
    comment = forms.CharField(widget=forms.Textarea, required=False, label='Комментарии')
    def __init__(self, *args, **kwargs):
        super(StatusThingForm, self).__init__(*args, **kwargs)
        self.fields['status'].empty_label="Выберите статус"
        self.fields['thing'].widget.attrs.update({'style': 'display:none'})
        self.fields['count'].initial = 1 
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
    def save(self, *args, **kwargs):
        super(StatusThingForm, self).save(*args, **kwargs)
        return self
    class Meta:
        model = StatusThing
        fields = '__all__'
        exclude = ('update',)