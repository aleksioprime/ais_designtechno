# Generated by Django 3.1.6 on 2021-02-14 21:50

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Thing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_manufacturer', models.CharField(max_length=255, verbose_name='Название от производителя')),
                ('manufacturer', models.CharField(max_length=255, null=True, verbose_name='Производитель')),
                ('name_bookkeeping', models.CharField(blank=True, max_length=255, null=True, verbose_name='Наимнование от бухгалтерии')),
                ('inventory_number', models.CharField(blank=True, max_length=16, null=True, verbose_name='Инвентарный номер')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Цена (руб)')),
                ('count', models.SmallIntegerField(default=1, verbose_name='Общее кол-во')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='thing_photo', verbose_name='Изображение предмета')),
                ('base_location', models.CharField(blank=True, max_length=255, null=True, verbose_name='Базовое местоположение')),
                ('photo_base_location', models.ImageField(blank=True, null=True, upload_to='thing_photo_location', verbose_name='Изображение предмета')),
            ],
            options={
                'verbose_name': 'Предмет',
                'verbose_name_plural': 'Предметы',
            },
        ),
        migrations.CreateModel(
            name='UseThings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False, verbose_name='Статус возврата')),
                ('count', models.SmallIntegerField(default=1, verbose_name='Количество')),
                ('justification', models.TextField(blank=True, null=True, verbose_name='Обоснование')),
                ('location', models.CharField(blank=True, max_length=255, null=True, verbose_name='Базовое местоположение')),
                ('created', models.DateField(default=datetime.date.today)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='use_employee', to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник')),
                ('thing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='use_thing', to='storage.thing', verbose_name='Предмет')),
            ],
            options={
                'verbose_name': 'Использование',
                'verbose_name_plural': 'Использование',
            },
        ),
        migrations.AddField(
            model_name='thing',
            name='employees',
            field=models.ManyToManyField(through='storage.UseThings', to=settings.AUTH_USER_MODEL, verbose_name='Сотрудники'),
        ),
    ]
