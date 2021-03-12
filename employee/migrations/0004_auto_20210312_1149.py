# Generated by Django 3.1.6 on 2021-03-12 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0004_auto_20210303_2255'),
        ('employee', '0003_lognotebook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lognotebook',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='loc_lognotebook', to='storage.location', verbose_name='Местоположение'),
        ),
    ]
