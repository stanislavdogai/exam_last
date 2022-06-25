from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext as _


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', verbose_name='Профиль',
                                on_delete=models.CASCADE)
    phone = PhoneNumberField(unique=True, region="KG", max_length=15, verbose_name=_('Номер телефона'))

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        db_table = 'profile_user'

    def __str__(self):
        return f'Профиль: {self.user.username}, {self.id}'