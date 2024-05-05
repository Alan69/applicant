import html
from django.db import models
from django.contrib.auth.models import User, Group
from datetime import timedelta, datetime
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
import os
from PIL import Image
from io import BytesIO
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from random import choice
from django.core.exceptions import ValidationError
from django.db.models import Count, F
from django.db import models
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.core.validators import RegexValidator
from django.conf import settings
import random
from django.core.exceptions import ValidationError
from django.utils.translation import get_language


class Faculty(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'))
    name_ru = models.TextField(verbose_name=_('Наименование на русском'))
    name_en = models.TextField(verbose_name=_('Наименование на английском'))

    class Meta:
        db_table = 'faculty'
        verbose_name = _('Факультет')
        verbose_name_plural = _('Факультеты')

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    faculty = models.ManyToManyField(
        Faculty, blank=True)
    groups = models.ManyToManyField(Group, blank=True, related_name='custom_users')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='custom_users')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}' if self.first_name and self.last_name else self.email


class CustomGroup(Group):
    # Добавьте поля для вашей настраиваемой модели группы
    pass


class EducationStage(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'))
    name_ru = models.TextField(verbose_name=_('Наименование на русском'))
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'education_stage'
        verbose_name = _('Ступень обучения')
        verbose_name_plural = _('Ступень обучения')

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)



class SpecialityGroup(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    education_stage = models.ForeignKey(
        EducationStage, on_delete=models.CASCADE, related_name='speciality_education_stage', null=True, blank=True,
        verbose_name='Ступень обучения')
    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, related_name='speciality_groups', verbose_name=_('Факультет'))
    cipher = models.CharField(max_length=100, verbose_name=_('Шифр'))
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'))
    name_ru = models.TextField(verbose_name=_('Наименование на русском'))
    name_en = models.TextField(verbose_name=_('Наименование на английском'))

    class Meta:
        db_table = 'speciality_group'
        verbose_name = _('Группа ОП')
        verbose_name_plural = _('Группа ОП')

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return f"{self.cipher} - {html.escape(name)}"
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return f"{self.cipher} - {html.escape(name)}"
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return f"{self.cipher} - {html.escape(name)}"



class Speciality(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    speciality_group = models.ForeignKey(
        SpecialityGroup, on_delete=models.CASCADE, related_name='speciality_group', verbose_name=_('Группа ОП'))
    cipher = models.CharField(max_length=100, verbose_name=_('Шифр'))
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'))
    name_ru = models.TextField(verbose_name=_('Наименование на русском'))
    name_en = models.TextField(verbose_name=_('Наименование на английском'))

    class Meta:
        db_table = 'speciality'
        verbose_name = _('Специальность')
        verbose_name_plural = _('Специальности')

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return f"{self.cipher} - {html.escape(name)}"
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return f"{self.cipher} - {html.escape(name)}"
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return f"{self.cipher} - {html.escape(name)}"


class Subject(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'), null=True, blank=True)
    name_ru = models.TextField(verbose_name=_('Наименование на русском'), null=True, blank=True)
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'subject'
        verbose_name = _('Предмет')
        verbose_name_plural = _('Предметы')

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class Subject1(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    speciality = models.ForeignKey(
        Speciality, on_delete=models.CASCADE, related_name='speciality_subject1', null=True, blank=True)
    subject1 = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='subject1', null=True, blank=True)

    class Meta:
        db_table = 'subject1'
        verbose_name = _('Предмет1')
        verbose_name_plural = _('Предметы1')

    def __str__(self):
        return str(self.subject1)


class Subject2(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    speciality = models.ForeignKey(
        Speciality, on_delete=models.CASCADE, related_name='speciality_subject2', null=True, blank=True)
    subject2 = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='subject2', null=True, blank=True)

    class Meta:
        db_table = 'subject2'
        verbose_name = _('Предмет2')
        verbose_name_plural = _('Предметы2')

    def __str__(self):
        return str(self.subject2)


class Country(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'), null=True, blank=True)
    name_ru = models.TextField(verbose_name=_('Наименование на русском'), null=True, blank=True)
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'country'
        verbose_name = _('Страна')
        verbose_name_plural = _('Страны')
        ordering = ['id']

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class Citizenship(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'), null=True, blank=True)
    name_ru = models.TextField(verbose_name=_('Наименование на русском'), null=True, blank=True)
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'citizenship'
        verbose_name = _('Гражданство')
        verbose_name_plural = _('Гражданство')
        ordering = ['id']

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class Nationality(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'), null=True, blank=True)
    name_ru = models.TextField(verbose_name=_('Наименование на русском'), null=True, blank=True)
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'nationality'
        verbose_name = _('Национальность')
        verbose_name_plural = _('Национальности')
        ordering = ['id']

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class Area(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'), null=True, blank=True)
    name_ru = models.TextField(verbose_name=_('Наименование на русском'), null=True, blank=True)
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'area'
        verbose_name = _('Область')
        verbose_name_plural = _('Области')

    def __str__(self):
        return str(self.external_id)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class Region(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    area = models.ForeignKey(
        Area, on_delete=models.CASCADE, related_name='area')
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'), null=True, blank=True)
    name_ru = models.TextField(verbose_name=_('Наименование на русском'), null=True, blank=True)
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'region'
        verbose_name = _('Регион')
        verbose_name_plural = _('Регионы')

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class EducationPeriod(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'))
    name_ru = models.TextField(verbose_name=_('Наименование на русском'))
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'education_period'
        verbose_name = _('Период')
        verbose_name_plural = _('Периоды')

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class PaymentForm(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'))
    name_ru = models.TextField(verbose_name=_('Наименование на русском'))
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'payment_form'
        verbose_name = _('Форма оплаты')
        verbose_name_plural = _('Форма оплаты')

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)



class EducationLevel(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'))
    name_ru = models.TextField(verbose_name=_('Наименование на русском'))
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'education_level'
        verbose_name = _('Уровень обучения')
        verbose_name_plural = _('Уровень обучения')

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class EducationForm(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'))
    name_ru = models.TextField(verbose_name=_('Наименование на русском'))
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'education_form'
        verbose_name = _('Форма обучения')
        verbose_name_plural = _('Форма обучения')

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class EducationLang(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'))
    name_ru = models.TextField(verbose_name=_('Наименование на русском'))
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'education_lang'
        verbose_name = _('Языковое отделение')
        verbose_name_plural = _('Языковое отделение')

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class EducationReason(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'))
    name_ru = models.TextField(verbose_name=_('Наименование на русском'))
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'education_reason'
        verbose_name = _('Основание для поступления')
        verbose_name_plural = _('Основание для поступления')

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class EducationReasonType(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'))
    name_ru = models.TextField(verbose_name=_('Наименование на русском'))
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'education_reason_type'
        verbose_name = _('Основание для зачисления')
        verbose_name_plural = _('Основание для зачисления')

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class EducationType(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'))
    name_ru = models.TextField(verbose_name=_('Наименование на русском'))
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'educational_type'
        verbose_name = _('Тип поступления')
        verbose_name_plural = _('Тип поступления')

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class Gender(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'), null=True, blank=True)
    name_ru = models.TextField(verbose_name=_('Наименование на русском'), null=True, blank=True)
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'gender'
        verbose_name = _('Пол')
        verbose_name_plural = _('Пол')

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class FamilyStatus(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'))
    name_ru = models.TextField(verbose_name=_('Наименование на русском'))
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'family_status'
        verbose_name = _('Семейное положение')
        verbose_name_plural = _('Семейное положение')

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class EducationInstitution(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'), null=True, blank=True)
    name_ru = models.TextField(verbose_name=_('Наименование на русском'), null=True, blank=True)
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'educational_institution'
        verbose_name = _('Тип учебного заведения')
        verbose_name_plural = _('Тип учебного заведения')

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class EducationCountry(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'), null=True, blank=True)
    name_ru = models.TextField(verbose_name=_('Наименование на русском'), null=True, blank=True)
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'educational_country'
        verbose_name = _('Страна, в которой закончил учебное заведение')
        verbose_name_plural = _('Страна, в которой закончил учебное заведение')

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class EducationPlaceStatus(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'), null=True, blank=True)
    name_ru = models.TextField(verbose_name=_('Наименование на русском'), null=True, blank=True)
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'educational_place_status'
        verbose_name = _('Статус населенного пункта')
        verbose_name_plural = _('Статус населенного пункта')

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class EducationCertificateType(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'), null=True, blank=True)
    name_ru = models.TextField(verbose_name=_('Наименование на русском'), null=True, blank=True)
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'educational_certificate_type'
        verbose_name = _('Тип документа')
        verbose_name_plural = _('Тип документа')

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class EducationCertificateProperties(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'), null=True, blank=True)
    name_ru = models.TextField(verbose_name=_('Наименование на русском'), null=True, blank=True)
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'educational_certificate_properties'
        verbose_name = _('Свойства документа')
        verbose_name_plural = _('Свойства документа')

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class DormitoryStatus(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'), null=True, blank=True)
    name_ru = models.TextField(verbose_name=_('Наименование на русском'), null=True, blank=True)
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'dormitory_status'
        verbose_name = _('Необходимо ли общежитие')
        verbose_name_plural = _('Необходимо ли общежитие')

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class ForeignLang(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'), null=True, blank=True)
    name_ru = models.TextField(verbose_name=_('Наименование на русском'), null=True, blank=True)
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'foreign_lang'
        verbose_name = _('Изучаемый иностранный язык')
        verbose_name_plural = _('Изучаемый иностранный язык')

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class FamilyPositionStatus(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'), null=True, blank=True)
    name_ru = models.TextField(verbose_name=_('Наименование на русском'), null=True, blank=True)
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'family_position_status'
        verbose_name = _('Семейный статус')
        verbose_name_plural = _('Семейный статус')

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class DocumentType(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'), null=True, blank=True)
    name_ru = models.TextField(verbose_name=_('Наименование на русском'), null=True, blank=True)
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'document_type'
        verbose_name = _('Документ, удостоверяющий личность')
        verbose_name_plural = _('Документ, удостоверяющий личность')

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class IdentificationIssuedBy(models.Model):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    name_kk = models.TextField(verbose_name=_('Наименование на казахском'), null=True, blank=True)
    name_ru = models.TextField(verbose_name=_('Наименование на русском'), null=True, blank=True)
    name_en = models.TextField(verbose_name=_('Наименование на английском'), null=True, blank=True)

    class Meta:
        db_table = 'identification_issued_by'
        verbose_name = _('Кем выдан')
        verbose_name_plural = _('Кем выдан')

    def __str__(self):
        return str(self.name)

    def __str__(self):
        lang = get_language()

        if lang == 'en':
            name = self.name_en if self.name_en else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        elif lang == 'kk':
            name = self.name_kk if self.name_kk else self.name_ru
            try:
                return html.escape(name)
            except:
                return ''
        else:
            name = self.name_ru if self.name_ru else _(
                'Отсутствует русское название')
            return html.escape(name)


class Proposal(models.Model):
    NEW = 'new'
    CHECKING = 'checking'
    ACCEPTED = 'accepted'
    ADDED = 'added'
    REJECTED = 'rejeted'  # TODO: Может rejected?

    statuses = [
        (NEW, 'Создана'),
        (CHECKING, 'На рассмотрении'),
        (ACCEPTED, 'Принята'),
        (ADDED, 'Добавлена'),
        (REJECTED, 'Отказана'),
    ]
    operator_reasons = [
        (ACCEPTED, 'Принята'),
    ]
    specialist_reasons = [
        (ACCEPTED, 'Принята'),
        (REJECTED, 'Отказана'),
    ]

    parent_types = [
        ('father', _('Отец')),
        ('Mother', _('Мать')),
        # TODO: Постарайся, чтобы типы были в одних реестрах (раз уж, father маленькими буквами, то и mother должен быть)
    ]

    levels = [
        ('А1', 'А1'),
        ('А2', 'А2'),
        ('В1', 'В1'),
        ('В2', 'В2'),
        ('С1', 'С1'),
        ('С2', 'С2'),
    ]

    conditionally_statuses = [
        ('yes', _('да')),
        ('no', _('нет')),
    ]

    discount_statuses = [
        ('my', _('Мой выбор YU')),
        ('sport', _('Спорт')),
        ('gold', _('Алтын белгі')),
    ]

    sport_statuses = [
        ('master', _('Мастер спорта')),
        ('kms', _('КМС')),
    ]

    percent_statuses = [
        ('25', _('25')),
        ('50', _('50')),
        ('75', _('75')),
        ('100', _('100')),
    ]

    NOT_SYNCED = 'not_synced'
    SYNCED = 'synced'
    ERROR = 'error'

    SYNC_STATUSES = (
        (NOT_SYNCED, _('Не синхронизирован')),
        (SYNCED, _('Синхронизирован')),
        (ERROR, _('Ошибка синхронизации')),
    )

    random_number = models.CharField(max_length=6, unique=True, blank=True, verbose_name='Идентификационный код')

    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')

    applicant = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='proposal_applicants'
    )

    middle_name = models.CharField(max_length=100, verbose_name='Отчество', null=True, blank=True)
    status = models.CharField(max_length=100, choices=statuses, default='new')

    first_name_en = models.CharField(max_length=100, verbose_name='Фамилия на английском')
    last_name_en = models.CharField(max_length=100, verbose_name='Имя на английском')
    middle_name_en = models.CharField(max_length=100, verbose_name='Отчество на английском', null=True, blank=True)
    phone_number = models.CharField(max_length=100, verbose_name='Номер телефона')

    education_period = models.ForeignKey(
        EducationPeriod, on_delete=models.CASCADE, related_name='proposal_education_period', null=True, blank=True,
        verbose_name='Период')
    education_type = models.ForeignKey(
        EducationType, on_delete=models.CASCADE, related_name='proposal_education_type', null=True, blank=True,
        verbose_name='Тип поступления')
    education_stage = models.ForeignKey(
        EducationStage, on_delete=models.CASCADE, related_name='proposal_education_stage', null=True, blank=True,
        verbose_name='Ступень обучения')
    education_level = models.ForeignKey(
        EducationLevel, on_delete=models.CASCADE, related_name='proposal_education_level', null=True, blank=True,
        verbose_name='Уровень обучения')
    education_reason = models.ForeignKey(
        EducationReason, on_delete=models.CASCADE, related_name='proposal_education_reason', null=True, blank=True,
        verbose_name='Основание для поступления')

    form_of_study = models.ForeignKey(
        EducationForm, on_delete=models.CASCADE, related_name='proposal_form_of_study', verbose_name='Форма обучения')
    lang_of_study = models.ForeignKey(
        EducationLang, on_delete=models.CASCADE, related_name='proposal_lang_of_study',
        verbose_name='Языковое отделение')
    payment_form = models.ForeignKey(
        PaymentForm, on_delete=models.CASCADE, related_name='proposal_payment_form', verbose_name='Форма оплаты')

    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, related_name='proposal_faculty', verbose_name='Факультет')
    educ_plan_group = models.ForeignKey(
        SpecialityGroup, on_delete=models.CASCADE, related_name='proposal_speciality_group',
        verbose_name='Группа специальности')
    educ_plan = models.ForeignKey(
        Speciality, on_delete=models.CASCADE, related_name='proposal_speciality', verbose_name='Специальности')

    citizenship = models.ForeignKey(
        Citizenship, on_delete=models.CASCADE, verbose_name='Гражданство')
    nationality = models.ForeignKey(
        Nationality, on_delete=models.CASCADE, verbose_name='Национальность')
    gender = models.ForeignKey(
        Gender, on_delete=models.CASCADE, verbose_name='Пол')
    family_status = models.ForeignKey(
        FamilyStatus, on_delete=models.CASCADE, verbose_name='Семейное положение')
    basis_for_enrollment = models.ForeignKey(
        EducationReasonType, on_delete=models.CASCADE, verbose_name='Основание для зачисления', null=True, blank=True)

    ict_number = models.CharField(max_length=100, verbose_name='ТЖК', null=True, blank=True)

    testing_certificate_date = models.DateField(verbose_name='Дата выдачи сертификата', null=True, blank=True)
    testing_certificate_series = models.CharField(max_length=100, verbose_name='Серия', null=True, blank=True)
    testing_certificate_number = models.CharField(max_length=100, verbose_name='Номер', null=True, blank=True)

    mathematical_literacy = models.IntegerField(verbose_name='Математическая грамотность', null=True, blank=True)
    reading_literacy = models.IntegerField(verbose_name='Грамотность чтения', null=True, blank=True)
    history_of_kazakhstan = models.IntegerField(verbose_name='История Казахстана', null=True, blank=True)

    profile_subject_1_name = models.ForeignKey(
        Subject1, on_delete=models.CASCADE, related_name='proposal_subject1',
        verbose_name='Профильный  предмет 1 наименование', null=True, blank=True)
    profile_subject_1 = models.IntegerField(verbose_name='Профильный  предмет 1 балл', null=True, blank=True)
    profile_subject_2_name = models.ForeignKey(
        Subject2, on_delete=models.CASCADE, related_name='proposal_subject2',
        verbose_name='Профильный  предмет 2 наименование', null=True, blank=True)
    profile_subject_2 = models.IntegerField(verbose_name='Профильный  предмет 2 балл', null=True, blank=True)

    competition_score = models.IntegerField(verbose_name='Балл конкурса', null=True, blank=True)

    grant_certificate_number = models.CharField(max_length=100, verbose_name='№ сертификата гранта', null=True,
                                                blank=True)
    grant_certificate_date = models.DateField(verbose_name='Дата выдачи сертификата', null=True, blank=True)

    educational_institution = models.ForeignKey(
        EducationInstitution, on_delete=models.CASCADE, related_name='proposal_educational_institution',
        verbose_name='Тип учебного заведения')
    institution_name = models.CharField(max_length=100, verbose_name='Название учебного заведения')
    educational_country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name='educational_country',
        verbose_name='Страна, в которой закончил учебное заведение')
    educational_area = models.ForeignKey(
        Area, on_delete=models.CASCADE, related_name='educational_area',
        verbose_name='Область месторасположения учебного заведения')
    educational_region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name='educational_region',
        verbose_name='Район месторасположения учебного заведения')
    educational_place_status = models.ForeignKey(
        EducationPlaceStatus, on_delete=models.CASCADE, related_name='educational_place_status',
        verbose_name='Статус населенного пункта, в котором находится учебное заведение')
    educational_certificate_type = models.ForeignKey(
        EducationCertificateType, on_delete=models.CASCADE, related_name='educational_place_status',
        verbose_name='Тип документа', null=True, blank=True)
    educational_certificate_properties = models.ForeignKey(
        EducationCertificateProperties, on_delete=models.CASCADE, related_name='educational_place_status',
        verbose_name='Свойства документа', null=True, blank=True)
    educational_certificate_date = models.DateField(verbose_name='Дата выдачи документа об образовании')
    educational_certificate_series = models.CharField(max_length=100, verbose_name='Серия')
    average_rating = models.IntegerField(verbose_name='Средняя оценка', null=True, blank=True)

    golden_badge = models.BooleanField(default=False, verbose_name='Алтын белгі', null=True, blank=True)
    golden_badge_file = models.FileField(upload_to='uploads/', null=True, blank=True)

    ielts_toefl_sertificate_file = models.FileField(upload_to='uploads/', null=True, blank=True)

    address_area = models.ForeignKey(
        Area, on_delete=models.CASCADE, related_name='address_area', verbose_name='Область')
    address_region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name='address_region', verbose_name='Район')
    address_city = models.CharField(max_length=100, verbose_name='село', null=True, blank=True)
    address_street = models.CharField(max_length=100, verbose_name='улица')
    address_house = models.CharField(max_length=100, verbose_name='дом')
    address_apartment = models.CharField(max_length=100, verbose_name='квартира')

    register_address_area = models.ForeignKey(
        Area, on_delete=models.CASCADE, related_name='register_address_area', verbose_name='Область')
    register_address_region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name='register_address_region', verbose_name='Район')
    register_address_city = models.CharField(max_length=100, verbose_name='село', null=True, blank=True)
    register_address_street = models.CharField(max_length=100, verbose_name='улица')
    register_address_house = models.CharField(max_length=100, verbose_name='дом')
    register_address_apartment = models.CharField(max_length=100, verbose_name='квартира')

    document_type = models.ForeignKey(
        DocumentType, on_delete=models.CASCADE, related_name='proposal_document_type', verbose_name='Тип документа')
    iin_regex = RegexValidator(
        regex=r'^\d{12}$',
        message="Номер должен содержать 12 цифр.'"
    )
    iin = models.CharField(validators=[iin_regex], max_length=12, verbose_name='ИИН')
    identification_number = models.CharField(max_length=12, verbose_name='Номер документа')
    identification_issued_by = models.ForeignKey(
        IdentificationIssuedBy, on_delete=models.CASCADE, related_name='proposal_identification_issued_by',
        verbose_name='Кем выдан')
    identification_issue_date = models.DateField(verbose_name='Дата выдачи')
    identification_expiration_date = models.DateField(verbose_name='Дата истечение срока ')
    identification_birth_date = models.DateField(verbose_name='дата рождения')
    identification_birth_country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name='birth_place', verbose_name='Страна рождения')
    identification_birth_place = models.CharField(max_length=100, verbose_name='Место рождения (по удостоверению)')

    family_position_status = models.ForeignKey(
        FamilyPositionStatus, on_delete=models.CASCADE, related_name='proposal_family_position_status',
        verbose_name='Семейный статус', null=True, blank=True)
    family_position_file = models.FileField(upload_to='uploads/', null=True, blank=True)

    parent_type = models.CharField(max_length=100, choices=parent_types, verbose_name='Тип родителей', null=True,
                                   blank=True)

    father_first_name = models.CharField(max_length=30, verbose_name='Имя Отца', null=True, blank=True)
    father_last_name = models.CharField(max_length=30, verbose_name='Фамилия Отца', null=True, blank=True)
    father_middle_name = models.CharField(max_length=100, verbose_name='Отчество Отца', null=True, blank=True)
    father_phone_number = models.CharField(max_length=100, verbose_name='Номер телефона Отца', null=True, blank=True)
    father_profession = models.CharField(max_length=100, verbose_name='Профессия Отца', null=True, blank=True)
    father_work = models.CharField(max_length=100, verbose_name='Место работы Отца', null=True, blank=True)

    mother_first_name = models.CharField(max_length=30, verbose_name='Имя Матери', null=True, blank=True)
    mother_last_name = models.CharField(max_length=30, verbose_name='Фамилия Матери', null=True, blank=True)
    mother_middle_name = models.CharField(max_length=100, verbose_name='Отчество Матери', null=True, blank=True)
    mother_phone_number = models.CharField(max_length=100, verbose_name='Номер телефона Матери', null=True, blank=True)
    mother_profession = models.CharField(max_length=100, verbose_name='Профессия Матери', null=True, blank=True)
    mother_work = models.CharField(max_length=100, verbose_name='Место работы Матери', null=True, blank=True)

    dormitory = models.ForeignKey(
        DormitoryStatus, on_delete=models.CASCADE, related_name='proposal_dormitory', verbose_name='Общежитие')

    english_level = models.ForeignKey(
        ForeignLang, on_delete=models.CASCADE, related_name='proposal_english_level',
        verbose_name='Изучаемый иностранный язык')

    discount_yu = models.CharField(max_length=100, choices=discount_statuses, verbose_name='Скидка', null=True,
                                   blank=True)
    discount_sport = models.CharField(max_length=100, choices=sport_statuses, verbose_name='Спорт', null=True,
                                      blank=True)
    discount_percent = models.CharField(max_length=100, choices=percent_statuses, verbose_name='Скидка %', null=True,
                                        blank=True)

    conditionally = models.CharField(max_length=100, choices=conditionally_statuses, verbose_name='Условно', null=True,
                                     blank=True)

    contract_file = models.FileField(upload_to='uploads/', verbose_name='Договор', null=True, blank=True)
    check_file = models.FileField(upload_to='uploads/', verbose_name='Чек', null=True, blank=True)

    operator_reason = models.CharField(max_length=100, choices=operator_reasons, null=True, blank=True,
                                       verbose_name='Статус оператора')
    specialist_reason = models.CharField(max_length=100, choices=specialist_reasons, null=True, blank=True,
                                         verbose_name='Статус специалиста')
    comment = models.TextField(null=True, blank=True)
    checker_operator = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, related_name='checker_operator', null=True, blank=True,
        verbose_name='Оператор')
    checker_specialist = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, related_name='checker_specialist', null=True, blank=True,
        verbose_name='Специалист')

    univer_id = models.IntegerField(null=True, blank=True, unique=True, verbose_name=_('Идентификатор из Univer'))
    sync_status = models.CharField(
        max_length=255, choices=SYNC_STATUSES, default=NOT_SYNCED, verbose_name=_('Статус синхронизации')
    )
    sync_comment = models.TextField(null=True, blank=True, verbose_name=_('Комментарии к статусу'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создании'))
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'proposal'
        verbose_name = _('Заявление')
        verbose_name_plural = _('Заявления')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['faculty']),
            models.Index(fields=['citizenship']),
            models.Index(fields=['nationality']),
            models.Index(fields=['educational_country']),
            models.Index(fields=['educ_plan']),
            models.Index(fields=['educ_plan_group']), 
        ]

    def save(self, *args, **kwargs):
        if not self.random_number:
            self.random_number = self.generate_unique_number()
        super().save(*args, **kwargs)

    def generate_unique_number(self):
        while True:
            # Генерация случайного числа из шести цифр
            random_number = str(random.randrange(100000, 999999))
            if not Proposal.objects.filter(random_number=random_number).exists():
                return random_number

    def __str__(self):
        full_name = ' '.join(filter(None, [self.last_name, self.first_name, self.middle_name]))
        return full_name

    @classmethod
    def export_resource_classes(cls):
        """
        Для асинхронного экспорта данных
        """
        from application.resources import ProposalResource

        return {
            'proposals': ('proposals', ProposalResource),
        }


@receiver(post_save, sender=Proposal)
def convert_attachment_heic_format(instance, *args, **kwargs):
    convert_heic_format(instance, *args, **kwargs)


@receiver(post_save, sender=Proposal)
def convert_heic_format(instance, *args, **kwargs):
    for field in instance._meta.fields:
        if type(field) == models.FileField:
            attr = getattr(instance, field.name)

            if not attr:
                continue

            if attr.path.endswith('.heif') or attr.path.endswith('.heic'):
                # heif_file = pyheif.read(attr.path)
                image = Image.frombytes(
                    # heif_file.mode,
                    # heif_file.size,
                    # heif_file.data,
                    # "raw",
                    # heif_file.mode,
                    # heif_file.stride,
                )
                filename = os.path.splitext(attr.name)[0]
                image_file = BytesIO()
                image.save(image_file, 'JPEG')
                attr.save('{}.jpg'.format(filename), image_file)
