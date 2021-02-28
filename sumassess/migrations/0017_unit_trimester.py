# Generated by Django 3.1.6 on 2021-02-17 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sumassess', '0016_remove_unit_subgroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='trimester',
            field=models.CharField(choices=[('I', 'I триместр'), ('II', 'II триместр'), ('III', 'III триместр')], default='I', max_length=3),
        ),
    ]
