from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db import models
from django.urls import reverse
import uuid


class MyUserManager(UserManager):
    
    def create_user(self, username, password=None, **kwargs):
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **kwargs):
        user = self.model(username=username, is_staff=True, is_superuser=True, **kwargs)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # На сервере при авторизации ошибка с uuid
    # id = models.UUIDField(default=uuid.uuid4, primary_key=True, verbose_name=_("Идентификатор"))
    username = models.CharField(_('Логин'), max_length=16, blank=False, unique=True)
    email = models.EmailField(_('E-Mail'), blank=True, unique=False)
    surname = models.CharField(_('Фамилия'), max_length=40, blank=True, null=True, unique=False)
    name = models.CharField(_('Имя'), max_length=40, blank=True, null=True, unique=False)
    patronymic = models.CharField(_('Отчество'), max_length=40, blank=True, null=True, unique=False)

    is_staff = models.BooleanField(
        _('Статус модератора'),
        default=False,
        help_text=_('Определяет, может ли пользователь войти на этот сайт администратора')
    )
    is_active = models.BooleanField(
        _('Активный'),
        default=True,
        help_text=_('Указывает, следует ли рассматривать этого пользователя как активного. Снимите этот флажок вместо удаления учетных записей')
    )
    date_joined = models.DateTimeField(_('Дата регистрации'), default=timezone.now)
    
    # дополнительные поля
    position = models.CharField(max_length=255, verbose_name=_("Должность"), default='Учитель')
    phone = models.CharField(max_length=12, verbose_name=_("Телефон"), null=True, blank=True)
    photo = models.ImageField(upload_to='employee_photo', blank=True, verbose_name=_("Фотография сотрудника"), null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        db_table = 'auth_user'
        abstract = False
        ordering = ['surname']

    def get_full_name(self):
        full_name = '%s %s' % (self.name, self.surname)
        return full_name.strip()

    def get_short_name(self):
        if self.name and self.patronymic:
            return "{} {}. {}.".format(self.surname, self.name[0], self.patronymic[0])
        else:
            return self.name
    
    def get_absolute_url(self):
        return reverse('employee:index') 

    def __str__(self):
        return "{} {}".format(self.name, self.surname)