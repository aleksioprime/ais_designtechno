from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
from datetime import date

class Programm(models.Model):
    """ Программы международного бакалавриата """
    label = models.CharField(max_length=3, verbose_name=_("Аббревиатура"))
    name_eng = models.CharField(max_length=255, verbose_name=_("Название на англ. языке"))
    name_rus = models.CharField(max_length=255, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    class Meta:
        verbose_name = 'IB Программа'
        verbose_name_plural = 'IB Программы'
    def __str__(self):
        return "{}".format(self.label)

class SubjectGroup(models.Model):
    """ Предметные группы (учебные дисциплины IB) """
    name_eng = models.CharField(max_length=32, verbose_name=_("Название на англ. языке"))
    name_rus = models.CharField(max_length=32, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    picture = models.ImageField(upload_to='subjectgroup_pic', blank=True, verbose_name=_("Картинка"), null=True)
    schema = models.ImageField(upload_to='subjectgroup_schema', blank=True, verbose_name=_("Схема"), null=True)
    programm = models.ForeignKey('sumassess.Programm', verbose_name=_("Программа IB"), on_delete=models.SET_NULL, \
        null=True, blank=False, related_name="subject_group")
    class Meta:
        verbose_name = 'Предметная группа IB'
        verbose_name_plural = 'Предметные группы IB'
    def __str__(self):
        return "{} - {}".format(self.name_eng, self.programm)

class Subject(models.Model):
    """ Учебные дисциплины """
    name_eng = models.CharField(max_length=32, verbose_name=_("Название на англ. языке"))
    name_rus = models.CharField(max_length=32, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    ibgroup = models.ForeignKey('sumassess.SubjectGroup', verbose_name=_("Предметная группа"), on_delete=models.SET_NULL, \
        null=True, blank=True, related_name="subject")
    class Meta:
        verbose_name = 'Учебная дисциплина'
        verbose_name_plural = 'Учебные дисциплины'
    def __str__(self):
        return "{} ({})".format(self.name_eng, self.ibgroup)

class Criteria(models.Model):
    """ Критерии оценивания с описанием """
    CRITERIA_LETTER = [
        ('A', 'Критерий A'),
        ('B', 'Критерий B'),
        ('C', 'Критерий C'),
        ('D', 'Критерий D'),
    ]
    letter = models.CharField(choices=CRITERIA_LETTER, max_length=1)
    name_eng = models.CharField(max_length=32, verbose_name=_("Название на англ. языке"))
    name_rus = models.CharField(max_length=32, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    picture = models.ImageField(upload_to='criteria_pic', blank=True, verbose_name=_("Картинка"), null=True)
    ibgroup = models.ForeignKey('sumassess.SubjectGroup', verbose_name=_("Предметная группа"), on_delete=models.SET_NULL, \
        null=True, blank=False, related_name="criteria")
    class Meta:
        verbose_name = 'Критерий оценивания'
        verbose_name_plural = 'Критерии оценивания'
        ordering = ['ibgroup', 'letter']
    def __str__(self):
        return "{}. {}".format(self.letter, self.name_eng)

class Strand(models.Model):
    """ Стрэнды - аспекты образовательных достижений """
    STRAND_LETTER = [
        (1, 'i'),
        (2, 'ii'),
        (3, 'iii'),
        (4, 'iv'),
    ]
    number = models.PositiveIntegerField(verbose_name=_("Абсолютный номер"), default=1)
    letter = models.PositiveIntegerField(choices=STRAND_LETTER, verbose_name=_("Метка в критерии"), default=1)
    name_eng = models.CharField(max_length=255, verbose_name=_("Название на англ. языке"))
    name_rus = models.CharField(max_length=255, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    shortname_eng = models.CharField(max_length=64, verbose_name=_("Краткое название на англ. языке"))
    shortname_rus = models.CharField(max_length=64, verbose_name=_("Краткое название на рус. языке"), null=True, blank=True)
    criteria = models.ForeignKey('sumassess.Criteria', verbose_name=_("Критерий"), on_delete=models.SET_NULL, \
        null=True, blank=False, related_name="strand")
    class Meta:
        verbose_name = 'Стрэнд'
        verbose_name_plural = 'Стрэнды'
        ordering = ['criteria', 'number', 'letter']
    def __str__(self):
        return "{} ({}). {} ({})".format(self.number, self.get_letter_display(), self.shortname_eng, self.criteria.ibgroup)

class ClassYear(models.Model):
    """ Годы обучения по международному бакалавриату """
    year_ib = models.CharField(max_length=32, verbose_name=_("Год обучения в IB"), null=True, blank=False)
    year_rus = models.PositiveIntegerField(verbose_name=_("Год обучения в РФ")) 
    programm = models.ForeignKey('sumassess.Programm', verbose_name=_("Программа IB"), on_delete=models.SET_NULL, \
        null=True, blank=False, related_name="class_year")
    class Meta:
        verbose_name = 'Год обучения'
        verbose_name_plural = 'Года обучения'
    def __str__(self):
        return "{} {}".format(self.programm, self.year_ib)

class Objective(models.Model):
    """ Образовательные цели """
    year = models.ForeignKey('sumassess.ClassYear', verbose_name=_("Год обучения в IB"), on_delete=models.SET_NULL, \
        null=True, blank=False, related_name="objective")
    strand = models.ForeignKey('sumassess.Strand', verbose_name=_("Стрэнд"), on_delete=models.SET_NULL, \
        null=True, blank=False, related_name="objective")
    name_eng = models.CharField(max_length=255,verbose_name=_("Описание на англ. языке"), null=True, blank=False)
    name_rus = models.CharField(max_length=255,verbose_name=_("Описание на рус. языке"), null=True, blank=True)
    class Meta:
        verbose_name = 'Образовательная цель'
        verbose_name_plural = 'Образовательные цели'
        ordering = ['year', 'strand']
    def __str__(self):
        return "{} - {} {}...".format(self.year, self.strand, self.name_eng[:10])

class Level(models.Model):
    """ Уровни достижений образовательных целей """
    objective = models.ForeignKey('sumassess.Objective', verbose_name=_("Образовательная цель"), on_delete=models.CASCADE, \
        null=True, blank=False, related_name="level")
    name_eng = models.TextField(verbose_name=_("Описание на англ. языке"), null=True, blank=False)
    name_rus = models.TextField(verbose_name=_("Описание на рус. языке"), null=True, blank=True)
    point = models.PositiveIntegerField(verbose_name=_("Баллы"), default=0)
    class Meta:
        verbose_name = 'Уровень достижений'
        verbose_name_plural = 'Уровни достижений'
        ordering = ['objective', 'point']
    def __str__(self):
        return "{}... - {}".format(self.name_eng[:30], self.point)