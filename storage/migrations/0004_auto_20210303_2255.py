# Generated by Django 3.1.6 on 2021-03-03 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0003_auto_20210303_2244'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='statusequipment',
            options={'verbose_name': 'Статус элемента', 'verbose_name_plural': 'Статусы элементов'},
        ),
        migrations.AlterField(
            model_name='status',
            name='info',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Пояснение'),
        ),
    ]
