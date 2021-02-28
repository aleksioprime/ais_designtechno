from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
from datetime import date

class SubjectGroup(models.Model):
    IB_PROGRAMM = [
        ('PYP', 'Primary Years Programme'),
        ('MYP', 'Middle Years Programme'),
        ('DP', 'Diploma Programme'),
    ]
    name = models.CharField(max_length=30, verbose_name=_("Название предметной области"))
    name_rus = models.CharField(max_length=30, verbose_name=_("Название на русском"))
    programm = models.CharField(choices=IB_PROGRAMM, default='MYP', max_length=3)
    class Meta:
        verbose_name = 'Предметная область'
        verbose_name_plural = 'Предметные области'
        ordering = ['programm', 'name']
    def __str__(self):
        return "{} {}".format(self.programm, self.name)
    def get_absolute_url(self):
        return reverse('sumassess:index') 

class Subject(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("Название предмета"))
    id_dnevnik = models.CharField(verbose_name=_('ID системы Дневник.РУ'), max_length=40, blank=True, null=True, unique=False)
    subjgroup = models.ForeignKey('sumassess.SubjectGroup', on_delete=models.SET_NULL, null=True, related_name="subject_sg")
    class Meta:
        verbose_name = 'Учебный предмет'
        verbose_name_plural = 'Учебные предметы'
        ordering = ['name']
    def __str__(self):
        return "{} ({})".format(self.name, self.subjgroup)
    def get_absolute_url(self):
        return reverse('sumassess:index') 

class YearIB(models.Model):
    IB_PROGRAMM = [
        ('PYP', 'Primary Years Programme'),
        ('MYP', 'Middle Years Programme'),
        ('DP', 'Diploma Programme'),
    ]
    year_ib = models.CharField(max_length=2, verbose_name=_("Год обучения в IB"))
    programm = models.CharField(choices=IB_PROGRAMM, default='MYP', max_length=3)
    grade_rus = models.CharField(max_length=2, verbose_name=_("Год обучения в РФ")) 
    class Meta:
        verbose_name = 'Год IB'
        verbose_name_plural = 'Года IB'
        ordering = ['programm', 'year_ib']
    def __str__(self):
        return "{} Year {} | {} класс".format(self.programm, self.year_ib, self.grade_rus)
    def get_absolute_url(self):
        return reverse('sumassess:index') 

class Criteria(models.Model):
    CRITERIA_LETTER = [
        ('A', 'Критерий A'),
        ('B', 'Критерий B'),
        ('C', 'Критерий C'),
        ('D', 'Критерий D'),
    ]
    subject = models.ForeignKey('sumassess.SubjectGroup', on_delete=models.SET_NULL, null=True, related_name="criteria_sub")
    letter = models.CharField(choices=CRITERIA_LETTER, default='A', max_length=1)
    name = models.CharField(max_length=255, verbose_name=_("Название критерия на английском"))
    name_rus = models.CharField(max_length=255, verbose_name=_("Название критерия на русском"), blank=True, null=True)
    class Meta:
        verbose_name = 'Критерий'
        verbose_name_plural = 'Критерии'
        ordering = ['subject', 'letter']
    def __str__(self):
        return "{}. {}".format(self.letter, self.name)
    def get_absolute_url(self):
        return reverse('sumassess:index') 

class Strand(models.Model):
    num = models.CharField(verbose_name=_("Номер"), max_length=2)
    letter = models.CharField(verbose_name=_("Буквенное обозначение"), max_length=3)
    name = models.CharField(max_length=255, verbose_name=_("Название стрэнда на английском"), blank=True, null=True)
    name_rus = models.CharField(max_length=255, verbose_name=_("Название стрэнда на русском"), blank=True, null=True)
    shortname = models.CharField(max_length=255, verbose_name=_("Краткое название стрэнда на английском"), blank=True, null=True)
    shortname_rus = models.CharField(max_length=255, verbose_name=_("Краткое название стрэнда на русском"), blank=True, null=True)
    criteria = models.ForeignKey('sumassess.Criteria', verbose_name=_("Критерий"), on_delete=models.CASCADE, null=True, related_name="strand_cri")
    class Meta:
        verbose_name = 'Cтрэнд'
        verbose_name_plural = 'Стрэнды'
        ordering = ['id', 'letter', 'name']
    def __str__(self):
        return "{}. {}".format(self.letter, self.shortname)

class Objective(models.Model):
    year_ib = models.ForeignKey('sumassess.YearIB', verbose_name=_("Год"), on_delete=models.CASCADE, null=True, related_name="objective_year")
    criteria = models.ForeignKey('sumassess.Criteria', verbose_name=_("Критерий"), on_delete=models.CASCADE, null=True, related_name="objective_cri")
    strand = models.ForeignKey('sumassess.Strand', verbose_name=_("Стрэнд"), on_delete=models.SET_NULL, null=True, related_name="objective_strand")
    name = models.TextField(verbose_name=_("Название цели на английском"), blank=True, null=True)
    name_rus = models.TextField(verbose_name=_("Название цели на русском"), blank=True, null=True)
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'
        ordering = ['year_ib', 'criteria', 'strand']
    def __str__(self):
        return "{} {} {} {}...".format(self.year_ib, self.criteria.letter, self.strand, self.name[:30])
    def get_absolute_url(self):
        return reverse('sumassess:index') 

class Level(models.Model):
    objective = models.ForeignKey('sumassess.Objective', verbose_name=_("Цель"), on_delete=models.CASCADE, null=True, related_name="level_objective")
    name = models.TextField(verbose_name=_("Название уровня на английском"), blank=True, null=True)
    name_rus = models.TextField(verbose_name=_("Название уровня на русском"), blank=True, null=True)
    point = models.PositiveIntegerField(verbose_name=_("Баллы"), default=0)
    class Meta:
        verbose_name = 'Уровень достижений'
        verbose_name_plural = 'Уровни достижений'
        ordering = ['objective', 'point', 'name']
    def __str__(self):
        return "{}. {}".format(self.name_rus, self.point)
    def get_absolute_url(self):
        return reverse('sumassess:index') 

class Unit(models.Model):
    styear = models.ForeignKey('sumassess.StudyYear', verbose_name=_('Учебный год'), related_name="unit_styear", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255, verbose_name=_("Название юнита"))
    year_ib = models.ForeignKey('sumassess.YearIB', verbose_name=_("Год"), on_delete=models.SET_NULL, null=True, related_name="unit_year")
    teacher = models.ForeignKey("employee.User", on_delete=models.SET_NULL, null=True, verbose_name=_("Учитель"), related_name="unit_teacher")
    subject = models.ForeignKey('sumassess.Subject', verbose_name=_("Предмет"), on_delete=models.SET_NULL, null=True, related_name="unit_subject")
    objective = models.ManyToManyField("sumassess.Objective", verbose_name=_("Выбранные цели"), blank=True, related_name="unit_objective")
    period = models.ForeignKey('sumassess.Period', verbose_name=_("Период"), on_delete=models.SET_NULL, null=True, related_name="unit_period")
    class Meta:
        verbose_name = 'Юнит'
        verbose_name_plural = 'Юниты'
        ordering = ['year_ib', 'period', 'subject']
    def __str__(self):
        return "{} {}".format(self.name, self.year_ib)
    def get_absolute_url(self):
        return reverse('sumassess:index')

class Student(models.Model):
    GENDER = [
        ('М', 'мужской'),
        ('Ж', 'женский'),
    ]
    shortname = models.CharField(verbose_name=_('Сокращённое имя'), max_length=12, null=True)
    surname = models.CharField(verbose_name=_('Фамилия'), max_length=40, blank=True, null=True)
    name = models.CharField(verbose_name=_('Имя'), max_length=40, blank=True, null=True)
    id_dnevnik = models.CharField(verbose_name=_('ID системы Дневник.РУ'), max_length=40, blank=True, null=True, unique=False)
    gender = models.CharField(choices=GENDER, verbose_name=_('Пол'), max_length=1, blank=True, null=True)
    group = models.ForeignKey('sumassess.Group', on_delete=models.SET_NULL, verbose_name=_('Класс'), blank=True, null=True, related_name="student_group")
    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['group', 'shortname']
    def __str__(self):
        return "{} {}".format(self.group, self.shortname)
    def get_absolute_url(self):
        return reverse('sumassess:index')

class Group(models.Model):
    year = models.ForeignKey('sumassess.YearIB', verbose_name=_('Год обучения'), related_name="group_year", on_delete=models.SET_NULL, null=True)
    styear = models.ForeignKey('sumassess.StudyYear', verbose_name=_('Учебный год'), related_name="group_styear", on_delete=models.SET_NULL, null=True)
    group_dnevnik = models.CharField(verbose_name=_('ID класса из Дневник.РУ'), max_length=40, blank=True, null=True)
    letter = models.CharField(verbose_name=_('Буква класса'), default='A', max_length=1)
    info = models.TextField(null=True, blank=True)
    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'
        ordering = ['year', 'letter']
    def __str__(self):
        return "{} {}".format(self.year, self.letter)
    def get_absolute_url(self):
        return reverse('sumassess:index')

class SubGroup(models.Model):
    name = models.CharField(verbose_name=_('Направление подгруппы'), max_length=40, blank=True, null=True, unique=False)
    group = models.ForeignKey("sumassess.Group", on_delete=models.SET_NULL, null=True, verbose_name=_("Класс"), related_name="subgroup_group")
    subject = models.ForeignKey("sumassess.Subject", on_delete=models.SET_NULL, null=True, verbose_name=_("Предмет"), related_name="subgroup_subject")
    teacher = models.ForeignKey("employee.User", on_delete=models.SET_NULL, null=True, verbose_name=_("Учитель"), related_name="subgroup_teacher")
    class Meta:
        verbose_name = 'Подгруппа'
        verbose_name_plural = 'Подгруппы'
        ordering = ['group', 'name']
    def __str__(self):
        return "{} ({}) {}".format(self.group, self.name, self.subject)
    def get_absolute_url(self):
        return reverse('sumassess:index')
    
class AssessmentUnit(models.Model):
    student = models.ForeignKey("sumassess.Student", on_delete=models.CASCADE, verbose_name=_("Студент"), related_name="assessment_student")
    unit = models.ForeignKey("sumassess.Unit", on_delete=models.CASCADE, verbose_name=_("Юнит"), related_name="assessment_unit")
    level = models.ManyToManyField("sumassess.Level", verbose_name=_("Выбранные уровни достижений"), related_name="assessment_level", blank=True, through="sumassess.AssessmentUnitLevel")
    mark_a = models.SmallIntegerField(verbose_name=_("Оценка по критерию A"), default=0)
    mark_b = models.SmallIntegerField(verbose_name=_("Оценка по критерию B"), default=0)
    mark_c = models.SmallIntegerField(verbose_name=_("Оценка по критерию C"), default=0)
    mark_d = models.SmallIntegerField(verbose_name=_("Оценка по критерию D"), default=0)
    comment = models.TextField(verbose_name=_("Комментарии"), null=True, blank=True)
    class Meta:
        verbose_name = 'Журнал оценивания'
        verbose_name_plural = 'Журналы оцениваний'
        ordering = ['unit', 'student']
    def __str__(self):
        return "{} ({})".format(self.student, self.unit)
    def get_absolute_url(self):
        return reverse('sumassess:index')
    
class AssessmentUnitLevel(models.Model):
    assessmentunit = models.ForeignKey("sumassess.AssessmentUnit", on_delete=models.CASCADE, verbose_name=_("Журнал юнита"), related_name="aul_assessuint")
    level = models.ForeignKey("sumassess.Level", on_delete=models.CASCADE, verbose_name=_("Уровень достижений"), related_name="aul_level")
    comment = models.TextField(verbose_name=_("Комментарии"), null=True, blank=True)
    class Meta:
        verbose_name = 'Выбор уровня'
        verbose_name_plural = 'Выборы уровней'
        ordering = ['assessmentunit', 'level']
    def __str__(self):
        return "{} - {}".format(self.assessmentunit, self.level)

class StudyYear(models.Model):
    year = models.CharField(verbose_name=_('Учебный год'), max_length=10)
    data_start = models.DateField(_("Дата начала учебного года"), null=True)
    data_end = models.DateField(_("Дата окончания учебного года"), null=True)
    class Meta:
        verbose_name = 'Учебный год'
        verbose_name_plural = 'Учебный года'
        ordering = ['year']
    def __str__(self):
        return "{}".format(self.year)
    def get_absolute_url(self):
        return reverse('sumassess:index')

class Period(models.Model):
    name = models.CharField(verbose_name=_('Название периода'), max_length=32)
    data_start = models.DateField(_("Дата начала периода"), null=True)
    data_end = models.DateField(_("Дата окончания периода"), null=True)
    id_dnevnik = models.CharField(verbose_name=_('ID системы Дневник.РУ'), max_length=40, blank=True, null=True, unique=False)
    styear = models.ForeignKey("sumassess.StudyYear", on_delete=models.CASCADE, verbose_name=_("Учебный год"), related_name="period_year", null=True)
    class Meta:
        verbose_name = 'Период'
        verbose_name_plural = 'Периоды'
        ordering = ['data_start']
    def __str__(self):
        return "{}".format(self.name)
    def get_absolute_url(self):
        return reverse('sumassess:index')