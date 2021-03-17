# Generated by Django 3.1.6 on 2021-03-17 15:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import employee.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=16, unique=True, verbose_name='Логин')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='E-Mail')),
                ('surname', models.CharField(blank=True, max_length=40, null=True, verbose_name='Фамилия')),
                ('name', models.CharField(blank=True, max_length=40, null=True, verbose_name='Имя')),
                ('patronymic', models.CharField(blank=True, max_length=40, null=True, verbose_name='Отчество')),
                ('is_staff', models.BooleanField(default=False, help_text='Определяет, может ли пользователь войти на этот сайт администратора', verbose_name='Статус модератора')),
                ('is_active', models.BooleanField(default=True, help_text='Указывает, следует ли рассматривать этого пользователя как активного. Снимите этот флажок вместо удаления учетных записей', verbose_name='Активный')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата регистрации')),
                ('position', models.CharField(default='Учитель', max_length=255, verbose_name='Должность')),
                ('phone', models.CharField(blank=True, max_length=12, null=True, verbose_name='Телефон')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='employee_photo', verbose_name='Фотография сотрудника')),
                ('id_card', models.CharField(blank=True, max_length=32, null=True, verbose_name='ID карты пропуска')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'db_table': 'auth_user',
                'ordering': ['surname'],
                'abstract': False,
            },
            managers=[
                ('objects', employee.models.MyUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='LogNoteBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Дата использования')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='emp_lognotebook', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Запись использования ноутбуков',
                'verbose_name_plural': 'Записи использования ноутбуков',
                'ordering': ['date'],
            },
        ),
    ]
