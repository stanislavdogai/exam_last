from django.db import models
from django.utils.translation import gettext as _

STATUS = [('moderated', 'На модерации'), ('public', 'Опубликовано'), ('cancel', 'Отклонено')]

class Category(models.Model):
    category = models.CharField(max_length=50, null=False, blank=False, verbose_name=_('Категория'))

    def __str__(self):
        return f'{self.id}. {self.category}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'categories'

class Ad(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Заголовок'))
    text = models.TextField(max_length=1000, null=False, blank=False, verbose_name=_('Описание'))
    category = models.ForeignKey('webapp.Category', on_delete=models.PROTECT, related_name='adds',
                                 null=False, blank=False, verbose_name=_('Категория'))
    image = models.ImageField(null=True, blank=True, upload_to='images/', verbose_name=_('Фотография'))
    price = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Цена'))
    status = models.CharField(max_length=25, choices=STATUS, default='moderated', null=False, blank=False, verbose_name=_('Статус'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))
    public_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Дата публикации'))
    author = models.ForeignKey('accounts.Profile', related_name='adds', null=False, blank=False,
                               on_delete=models.PROTECT, verbose_name=_('Автор'))
    is_deleted = models.BooleanField(null=True, blank=True, default=False, verbose_name=_('Удален'))

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        db_table = 'adds'

class Comment(models.Model):
    ad = models.ForeignKey('webapp.Ad', on_delete=models.CASCADE, related_name='comments',
                           null=False, blank=False, verbose_name=_('Объявление'))
    author = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='comments_author',
                               null=False, blank=False, verbose_name=_('Автор'))
    text = models.CharField(max_length=300, null=False, blank=False, verbose_name=_('Комментарий'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата публикации'))

    def __str__(self):
        return f"{self.author}: {self.text}"

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        db_table = 'comments'