# Generated by Django 3.1.6 on 2021-04-05 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sumassess', '0002_auto_20210405_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='criteria',
            name='letter',
            field=models.CharField(choices=[('A', 'Критерий A'), ('B', 'Критерий B'), ('C', 'Критерий C'), ('D', 'Критерий D')], max_length=1),
        ),
    ]
