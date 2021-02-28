from django import forms
from employee.models import User
from datetime import date

class UserForm(forms.ModelForm):            
        username = forms.CharField(required=False, max_length=15, label='Логин', disabled=True,)
        surname = forms.CharField(required=False, max_length=40, label='Фамилия')
        name = forms.CharField(required=False, max_length=40, label='Имя')
        patronymic = forms.CharField(required=False, max_length=40, label='Отчество')
        email = forms.CharField(required=False, max_length=40, label='E-mail')
        position = forms.CharField(required=False, max_length=255, label='Должность')
        phone = forms.CharField(required=False, max_length=12, label='Телефон')
        photo = forms.ImageField(label='Загрузка фотографии', required=False)

        def __init__(self, *args, **kwargs):
            super(UserForm, self).__init__(*args, **kwargs)
            for field in iter(self.fields):
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                })

            self.fields['email'].widget.attrs['placeholder'] = 'namesurname@sk.ru'
            self.fields['username'].widget.attrs['placeholder'] = 'Введите фамилию'

            # if self.instance.pk:
            #     self.fields['username'].required = False
            #     self.fields['username'].widget.attrs['readonly'] = True

        def save(self, *args, **kwargs):
            self.date_joined = date.today()
            super(UserForm, self).save(*args, **kwargs)
            return self

        class Meta:
            model = User
            fields = ['username', 'surname', 'name', 'patronymic', 'email', 'position', 'phone', 'photo']