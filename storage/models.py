from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
from datetime import date
from django.contrib.postgres.fields import ArrayField

# Таблица кабинетов учебного заведения (заполняется модератором через админку)
class Cabinet(models.Model):
    label = models.CharField(max_length=16, verbose_name=_("№/метка"))
    name = models.CharField(max_length=64, verbose_name=_("Название"))
    photo = models.ImageField(upload_to='cabinet_photo', blank=True, verbose_name=_("Фотография кабинета"), null=True)
    coordinates = models.URLField(verbose_name=_("Ссылка на координаты"), null=True, blank=True)
    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'
        ordering = ['label']
    def __str__(self):
            return "{}".format(self.label)

# Таблица местоположений (будет заполняться автоматически)
# class Location(models.Model):
#     name = models.CharField(max_length=255, verbose_name=_("Описание"))
#     cabinet = models.ForeignKey("storage.Cabinet", on_delete=models.SET_NULL, verbose_name=_("Кабинет"), related_name="loc", null=True, blank=True)
#     photo = models.ImageField(upload_to='location_photo', blank=True, verbose_name=_("Фотография местоположения"), null=True)
#     class Meta:
#         verbose_name = 'Местоположение'
#         verbose_name_plural = 'Местоположения'
#         ordering = ['cabinet','name']
#     def __str__(self):
#             return "{} {}".format(self.name, self.cabinet)

# Таблица статусов (заполняется модератором через админку)
class Status(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Статус"))
    picture = models.ImageField(upload_to='status_picture', blank=True, verbose_name=_("Картинка"), null=True)
    note = models.TextField(verbose_name=_("Описание"), null=True, blank=True)
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
    def __str__(self):
        return "{}".format(self.name)

# Таблица присвоений статусов
class StatusThing(models.Model):
    thing = models.ForeignKey("storage.Thing", on_delete=models.CASCADE, verbose_name=_("Предмет"), related_name="status_thing")
    status = models.ForeignKey("storage.Status", on_delete=models.CASCADE, verbose_name=_("Статус"), related_name="status_thing")
    count = models.SmallIntegerField(verbose_name=_("Количество"), default=1)
    comment = models.TextField(verbose_name=_("Комментарий"), null=True, blank=True)
    update = models.DateField(verbose_name=_("Дата обновления статуса"), default=date.today)
    class Meta:
        verbose_name = 'Присвоение статусов'
        verbose_name_plural = 'Присвоение статусов'
    def __str__(self):
        return "{}".format(self.thing, self.status)

# Таблица предметов
class Thing(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Наименование"))
    name_docs = models.CharField(max_length=255, verbose_name=_("Наименование по документам"), null=True, blank=True)
    inventory = models.CharField(max_length=255, verbose_name=_("Инвентарные номера"), null=True, blank=True)
    manufacturer = models.CharField(max_length=255, verbose_name=_("Производитель"), null=True)
    site = models.URLField(verbose_name=_("Ссылка на web-страницу"), null=True, blank=True)
    description = models.TextField(verbose_name=_("Описание"), null=True, blank=True)
    comment = models.TextField(verbose_name=_("Комментарии"), null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name=_("Цена (руб)"))
    count = models.SmallIntegerField(verbose_name=_("Общее кол-во"), default=True)
    picture = models.ImageField(upload_to='thing_picture', blank=True, verbose_name=_("Изображение"), null=True)
    photo = models.ImageField(upload_to='thing_photo', blank=True, verbose_name=_("Фотография"), null=True)
    is_accounting = models.BooleanField(verbose_name=_("Бухгалтерский учёт"), default=False)
    is_material = models.BooleanField(verbose_name=_("Расходный материал"), default=False)
    is_set = models.BooleanField(verbose_name=_("Набор"), default=False)
    person = models.ForeignKey("employee.User", on_delete = models.SET_NULL, related_name="thing_person", verbose_name=_("Ответственный сотрудник"), null=True, blank=True)
    # location = models.OneToOneField("storage.Location", on_delete = models.SET_NULL, related_name="thing", verbose_name=_("Местоположение"), null=True, blank=True)
    loc_name = models.CharField(max_length=255, verbose_name=_("Описание местоположения"), null=True, blank=True)
    loc_cabinet = models.ForeignKey("storage.Cabinet", on_delete=models.SET_NULL, verbose_name=_("Кабинет"), related_name="thing", null=True, blank=True)
    loc_photo = models.ImageField(upload_to='location_photo', blank=True, verbose_name=_("Фотография местоположения"), null=True)
    employees = models.ManyToManyField("employee.User", verbose_name=_("Сотрудники"), through="storage.UseThing")
    composition = models.ManyToManyField("storage.Thing", verbose_name=_("Элементы"), through="storage.Composition")
    statuses = models.ManyToManyField("storage.Status", verbose_name=_("Статусы"), through="storage.StatusThing")
    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['name']
    def __str__(self):
            return self.name
    def get_id(self):
        return "{:05}".format(self.id)

# Таблица использования предметов
class UseThing(models.Model):
    thing = models.ForeignKey("storage.Thing", on_delete=models.CASCADE, verbose_name=_("Предмет"), related_name="use")
    employee = models.ForeignKey("employee.User", on_delete=models.CASCADE, verbose_name=_("Сотрудник"), related_name="use")
    # location = models.OneToOneField("storage.Location", on_delete = models.SET_NULL, related_name="use", verbose_name=_("Местоположение"), null=True, blank=True)
    loc_name = models.CharField(max_length=255, verbose_name=_("Описание местоположения"), null=True, blank=True)
    loc_cabinet = models.ForeignKey("storage.Cabinet", on_delete=models.SET_NULL, verbose_name=_("Кабинет"), related_name="use", null=True, blank=True)
    loc_photo = models.ImageField(upload_to='location_photo', blank=True, verbose_name=_("Фотография местоположения"), null=True)
    count = models.SmallIntegerField(verbose_name=_("Количество"), default=1)
    justification = models.TextField(verbose_name=_("Обоснование"), null=True, blank=True)
    created = models.DateField(default=date.today)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Использование предметов'
        verbose_name_plural = 'Использование предметов'
    def __str__(self):
        return "{} {}".format(self.thing, self.employee)

# Таблица элементов (принадлежности предметов к наборам)
class Composition(models.Model):
    thing = models.ForeignKey("storage.Thing", on_delete=models.CASCADE, verbose_name=_("Предмет"), related_name="eq_thing")
    equipment = models.ForeignKey("storage.Thing", on_delete=models.CASCADE, verbose_name=_("Элемент"), related_name="eq_equip")
    count = models.SmallIntegerField(verbose_name=_("Количество"), default=1)
    class Meta:
        verbose_name = 'Состав'
        verbose_name_plural = 'Составы'
        ordering = ['thing']
    def __str__(self):
        return "{} {}".format(self.thing, self.equipment)
