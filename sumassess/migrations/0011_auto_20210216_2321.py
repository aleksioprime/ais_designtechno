# Generated by Django 3.1.6 on 2021-02-16 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sumassess', '0010_auto_20210216_2312'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subject',
            options={'ordering': ['name'], 'verbose_name': 'Учебный предмет', 'verbose_name_plural': 'Учебные предметы'},
        ),
        migrations.AlterModelOptions(
            name='subjectgroup',
            options={'ordering': ['programm', 'name'], 'verbose_name': 'Предметная область', 'verbose_name_plural': 'Предметные области'},
        ),
        migrations.AddField(
            model_name='subgroup',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subgroup_subject', to='sumassess.subject', verbose_name='Предмет'),
        ),
    ]
