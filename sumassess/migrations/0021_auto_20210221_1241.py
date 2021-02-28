# Generated by Django 3.1.6 on 2021-02-21 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sumassess', '0020_remove_student_subgroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(blank=True, choices=[('М', 'мужской'), ('Ж', 'женский')], max_length=1, null=True, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='student',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_group', to='sumassess.group', verbose_name='Класс'),
        ),
    ]
