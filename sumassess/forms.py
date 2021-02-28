from django import forms
from employee.models import User
from sumassess.models import AssessmentUnit, Level, Unit, Objective, StudyYear, YearIB, Subject, Period

# class CustomMMCF(forms.ModelMultipleChoiceField):
#     def label_from_instance(self, objective):
#         return "{} {}. {}".format(objective.criteria.letter, objective.strand.letter, objective.name_rus) 

class CustomModelChoiceIterator(forms.models.ModelChoiceIterator):
    def choice(self, obj):
        return (self.field.prepare_value(obj),
                self.field.label_from_instance(obj), obj)

class CustomModelChoiceField(forms.models.ModelMultipleChoiceField):
    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return CustomModelChoiceIterator(self)
    choices = property(_get_choices, forms.MultipleChoiceField._set_choices)

# class AssessmentUnitForm(forms.ModelForm):       
#     level = CustomMMCF(queryset=Level.objects.all(), widget=forms.CheckboxSelectMultiple)
#     mark_ib = forms.DecimalField(widget=forms.NumberInput, required=True, label='Количество', decimal_places=0, min_value=1)
#     def __init__(self, *args, **kwargs):
#         super(AssessmentUnitForm, self).__init__(*args, **kwargs)
#         self.fields['mark_ib'].widget.attrs['value'] = 0

#     def save(self, *args, **kwargs):
#         super(AssessmentUnitForm, self).save(*args, **kwargs)
#         return self

#     class Meta:
#         model = AssessmentUnit
#         fields = ['student', 'unit', 'level', 'mark_ib']

class UnitForm(forms.ModelForm):
    styear = forms.ModelChoiceField(queryset=StudyYear.objects.all(), required=True, label='Учебный год')
    name = forms.CharField(widget=forms.TextInput, required=True, label='Название юнита')
    year_ib = forms.ModelChoiceField(queryset=YearIB.objects.all(), required=True, label='Год обучения')
    teacher = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label='Учитель')
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), required=True, label='Предмет')
    period = forms.ModelChoiceField(queryset=Period.objects.all(), required=True, label='Период')
    # objective = CustomMMCF(queryset=Objective.objects.all(), widget=forms.CheckboxSelectMultiple, required=False, label='Цели')
    objective = CustomModelChoiceField(queryset=Objective.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    def __init__(self,  *args, **kwargs):
        super(UnitForm, self).__init__(*args, **kwargs)
        
        if 'year_ib' in kwargs['initial']:
            self.fields['year_ib'].initial = kwargs['initial']['year_ib']
        if 'year_ib' in kwargs['initial']:
            self.fields['objective'].queryset = Objective.objects.filter(year_ib=kwargs['initial']['year_ib'])
            self.fields['year_ib'].widget.attrs.update({'style': 'display:none'})
        else:
            self.fields['year_ib'].widget.attrs.update({'style': 'display:true'})
        if 'year' in kwargs['initial']:
            self.fields['styear'].initial = kwargs['initial']['year']
        if 'user' in kwargs['initial']:
            self.fields['teacher'].initial = kwargs['initial']['user']
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['styear'].widget.attrs.update({'class': 'form-control'})
        self.fields['styear'].empty_label=None
        self.fields['year_ib'].widget.attrs.update({'class': 'form-control'})
        self.fields['year_ib'].empty_label="Выберите год в IB"
        self.fields['subject'].widget.attrs.update({'class': 'form-control'})
        self.fields['subject'].empty_label="Выберите предмет"
        self.fields['period'].widget.attrs.update({'class': 'form-control'})
        self.fields['period'].empty_label="Выберите период обучения"
        self.fields['teacher'].widget.attrs.update({'class': 'form-control'})
        self.fields['teacher'].widget.attrs.update({'style': 'display:none'})
        
    def save(self, *args, **kwargs):
        super(UnitForm, self).save(*args, **kwargs)
        # self.teacher = User.objects.get(id=self.request.user.id)
        return self

    class Meta:
        model = Unit
        fields = ['styear', 'name', 'year_ib', 'teacher', 'subject', 'objective', 'period']