# Generated by Django 3.1.6 on 2021-04-05 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sumassess', '0004_auto_20210405_2000'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='strand',
            options={'ordering': ['criteria', 'number', 'letter'], 'verbose_name': 'Стрэнд', 'verbose_name_plural': 'Стрэнды'},
        ),
        migrations.AlterField(
            model_name='objective',
            name='name_eng',
            field=models.CharField(max_length=255, null=True, verbose_name='Описание на англ. языке'),
        ),
        migrations.AlterField(
            model_name='objective',
            name='name_rus',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Описание на рус. языке'),
        ),
    ]