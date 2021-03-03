from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
from datetime import date

class Status(models.Model):
    name = models.CharField(max_length=32, verbose_name=_("Название"))
    info = models.CharField(max_length=255, verbose_name=_("Пояснение"), null=True, blank=True)
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        ordering = ['name']
    def __str__(self):
            return "{}".format(self.name)

class Location(models.Model):
    label = models.CharField(max_length=16, verbose_name=_("№/метка"))
    name = models.CharField(max_length=64, verbose_name=_("Название"))
    photo_map = models.ImageField(upload_to='location_photo', blank=True, verbose_name=_("Изображение кабинета на плане"), null=True)
    url_coord = models.URLField(verbose_name=_("Ссылка на координаты"), null=True, blank=True)
    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'
        ordering = ['label']
    def __str__(self):
            return "{}".format(self.label)

class Thing(models.Model):
    name_manufacturer = models.CharField(max_length=255, verbose_name=_("Название от производителя"))   
    manufacturer = models.CharField(max_length=255, verbose_name=_("Производитель"), null=True)
    url_site = models.URLField(verbose_name=_("Ссылка на web-страницу"), null=True, blank=True)
    name_bookkeeping = models.CharField(max_length=255, verbose_name=_("Наименование от бухгалтерии"), null=True, blank=True)
    inventory_number = models.CharField(max_length=16, verbose_name=_("Инвентарный номер"), null=True, blank=True)
    description = models.TextField(verbose_name=_("Описание"), null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name=_("Цена (руб)"))
    count = models.SmallIntegerField(verbose_name=_("Общее кол-во"), default=1)
    photo = models.ImageField(upload_to='thing_photo', blank=True, verbose_name=_("Изображение предмета"), null=True)
    base_location = models.ForeignKey("storage.Location", on_delete=models.SET_NULL, verbose_name=_("Местоположение/кабинет"), related_name="loc_thing", null=True, blank=True)
    photo_base_location = models.ImageField(upload_to='thing_photo_location', blank=True, verbose_name=_("Фотография метонахождения"), null=True)
    employees = models.ManyToManyField("employee.User", verbose_name=_("Сотрудники"), through="storage.UseThings")
    finresp = models.ForeignKey("employee.User", on_delete=models.SET_NULL, verbose_name=_("Материально-ответственное лицо"), related_name="finresp_thing", null=True, blank=True)
    comment = models.TextField(verbose_name=_("Комментарии"), null=True, blank=True)
    equipments = models.ManyToManyField("storage.Equipment", verbose_name=_("Сотрудники"), through="storage.CompositionEquipment")
    status = models.ForeignKey("storage.Status", on_delete=models.SET_NULL, verbose_name=_("Статус"), related_name="status_thing", null=True, blank=True)
    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'
        ordering = ['name_manufacturer']
    def __str__(self):
            return self.name_manufacturer
    def get_absolute_url(self):
        return reverse('storage:things') 
    def get_id(self):
        return "{:05}".format(self.id)
    def get_invnumber(self):
        if self.inventory_number is not None: 
            if self.inventory_number.isdigit():
                return "{:09}".format(int(self.inventory_number))
            else:
                return self.inventory_number
        else:
            return "-"

class UseThings(models.Model):
    thing = models.ForeignKey("storage.Thing", on_delete=models.CASCADE,
                             verbose_name=_("Предмет"),
                             related_name="use_thing")
    employee = models.ForeignKey("employee.User", on_delete=models.CASCADE,
                               verbose_name=_("Сотрудник"),
                               related_name="use_employee")
    count = models.SmallIntegerField(verbose_name=_("Количество"), default=1)
    justification = models.TextField(verbose_name=_("Обоснование"), null=True, blank=True)
    location = models.CharField(max_length=255, verbose_name=_("Базовое местоположение"), blank=True, null=True) 
    created = models.DateField(default=date.today)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Использование'
        verbose_name_plural = 'Использование'
    def __str__(self):
        return "-".join((str(self.thing),
                         str(self.employee),
                         str(self.count),))

class Equipment(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Наименование"))
    photo = models.ImageField(upload_to='equipment_photo', blank=True, verbose_name=_("Изображение элемента"), null=True)
    info = models.TextField(verbose_name=_("Информация"), null=True, blank=True)
    class Meta:
        verbose_name = 'Элемент'
        verbose_name_plural = 'Элементы'
        ordering = ['name']
    def __str__(self):
        return self.name

class CompositionEquipment(models.Model):
    equipment = models.ForeignKey("storage.Equipment", on_delete=models.CASCADE, verbose_name=_("Элемент"), related_name="copmpos_equipment")
    thing = models.ForeignKey("storage.Thing", on_delete=models.CASCADE, verbose_name=_("Позиция"), related_name="compos_thing")
    count = models.SmallIntegerField(verbose_name=_("Кол-во"), default=1)
    class Meta:
        verbose_name = 'Состав'
        verbose_name_plural = 'Составы'
    def __str__(self):
        return "-".join((str(self.equipment),
                        str(self.thing)))

class StatusEquipment(models.Model):
    equipment = models.ForeignKey("storage.Equipment", on_delete=models.CASCADE, verbose_name=_("Элемент"), related_name="status_equipment")
    name = models.CharField(max_length=255, verbose_name=_("Статус"))
    note = models.CharField(max_length=255, verbose_name=_("Примечание"), blank=True)
    count = models.SmallIntegerField(verbose_name=_("Кол-во"), default=1)
    user = models.ForeignKey("employee.User", on_delete=models.CASCADE, verbose_name=_("Пользователь"), related_name="status_employee", null=True, blank=True)
    class Meta:
        verbose_name = 'Статус элемента'
        verbose_name_plural = 'Статусы элементов'
    def __str__(self):
        return "-".join((str(self.name),
                         str(self.user)))
