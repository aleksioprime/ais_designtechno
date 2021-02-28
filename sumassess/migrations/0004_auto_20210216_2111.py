# Generated by Django 3.1.6 on 2021-02-16 18:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sumassess', '0003_auto_20210216_2049'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['year', 'letter'], 'verbose_name': 'Класс', 'verbose_name_plural': 'Классы'},
        ),
        migrations.RemoveField(
            model_name='group',
            name='cl',
        ),
        migrations.AddField(
            model_name='group',
            name='info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='year',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group_year', to='sumassess.yearib', verbose_name='Год обучения'),
        ),
        migrations.AddField(
            model_name='strand',
            name='criteria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='strand_cri', to='sumassess.criteria', verbose_name='Критерий'),
        ),
        migrations.AlterField(
            model_name='criteria',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='criteria_sub', to='sumassess.subject'),
        ),
        migrations.AlterField(
            model_name='level',
            name='objective',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='level_objective', to='sumassess.objective', verbose_name='Цель'),
        ),
        migrations.AlterField(
            model_name='objective',
            name='criteria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='objective_cri', to='sumassess.criteria', verbose_name='Критерий'),
        ),
        migrations.AlterField(
            model_name='objective',
            name='strand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='objective_strand', to='sumassess.strand', verbose_name='Стрэнд'),
        ),
        migrations.AlterField(
            model_name='objective',
            name='year_ib',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='objective_year', to='sumassess.yearib', verbose_name='Год'),
        ),
        migrations.AlterField(
            model_name='student',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_group', to='sumassess.group', verbose_name='Класс'),
        ),
        migrations.AlterField(
            model_name='student',
            name='subgroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_subgroup', to='sumassess.subgroup', verbose_name='Группа'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='unit_subject', to='sumassess.subject', verbose_name='Предмет'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='unit_teacher', to=settings.AUTH_USER_MODEL, verbose_name='Учитель'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='year_ib',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='unit_year', to='sumassess.yearib', verbose_name='Год'),
        ),
    ]
