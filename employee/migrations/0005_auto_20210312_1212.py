# Generated by Django 3.1.6 on 2021-03-12 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_auto_20210312_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lognotebook',
            name='date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата использования'),
        ),
    ]
