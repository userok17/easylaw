from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.
class Category(models.Model):
    ''' Категории бланков '''
    title = models.CharField('Название категории', max_length=200)
    description = models.TextField('Описание', null=True, blank=True)
    date_added = models.DateTimeField('Дата добавления', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['date_added']
    
    def __str__(self):
        return self.title
    
class Blank(models.Model):
    ''' Бланк документа '''
    category = models.ForeignKey(Category, verbose_name='Категория')
    title = models.CharField('Название бланка', max_length=200)
    description = models.TextField('Описание', null=True, blank=True)
    text = models.TextField('Текст бланка', null=True, blank=True)
    date_added = models.DateTimeField('Дата добавления', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Бланк'
        verbose_name_plural = 'Бланки'
        ordering = ['date_added']
    
    def __str__(self):
        return self.title

class Bookmark(models.Model):
    ''' Закладки '''
    user = models.ForeignKey(User, verbose_name='Пользователь')
    blank = models.ForeignKey(Blank, verbose_name='Бланк')
    date_added = models.DateTimeField('Дата добавления',  auto_now_add=True)
    
    class Meta:
        verbose_name = 'Закладка'
        verbose_name_plural = 'Закладки'
        ordering = ['-date_added']
    
    def fullname(self):
        return self.user.get_full_name()
    
    fullname.short_description = 'Имя и Фамилия'
    fullname.allow_tags = True
    
    def __str__(self):
        return '{} {}'.format(self.user, self.blank)


    
class Comment(models.Model):
    ''' Комментарии текущего бланка '''
    author = models.ForeignKey(User, verbose_name='Автор комментария')
    blank = models.ForeignKey(Blank, verbose_name='Название бланка')
    date_added = models.DateTimeField('Дата добавления', auto_now_add=True)
    body = models.TextField('Текст')
    
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-date_added']

    def fullname(self):
        return self.author.get_full_name()
    
    fullname.short_description = 'Имя и Фамилия'
    fullname.allow_tags = True
    
    def __str__(self):
        return '{} {}: {}'.format(self.author.first_name, self.author.last_name, self.body)
    
    