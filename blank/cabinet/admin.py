from django.contrib import admin
from django import forms
from .models import Category, Blank, Comment, Bookmark

# Register your models here.
@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    ''' Категории '''
    class Media:
        js = ('http://cdn.tinymce.com/4/tinymce.min.js',
              '/static/js/tiny_mce/tinymce_init.js',
              '/static/js/tiny_mce/tag_editable.js')
    list_display = ['title', 'date_added']
    search_fields = ['title', 'text']

@admin.register(Blank)
class AdminBlank(admin.ModelAdmin):
    ''' Бланки '''
    class Media:
        js = ('http://cdn.tinymce.com/4/tinymce.min.js',
              '/static/js/tiny_mce/tinymce_init.js',
              '/static/js/tiny_mce/tag_editable.js')
    list_display = ['title', 'date_added']
    search_fields = ['title', 'text']
    

class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return '{} {}'.format(obj.last_name, obj.first_name)



@admin.register(Bookmark)
class AdminBookmark(admin.ModelAdmin):
    ''' Комментарии к бланкам '''
    list_display = ['blank', 'fullname', 'date_added']
    
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):    
        if db_field.name == 'user':
            kwargs['form_class'] = UserChoiceField
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    ''' Комментарии к бланкам '''
    list_display = ['blank', 'fullname', 'date_added', 'body']
    
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):    
        if db_field.name == 'author':
            kwargs['form_class'] = UserChoiceField
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
