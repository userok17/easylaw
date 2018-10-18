from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from weasyprint import HTML
from io import BytesIO
from django.http import HttpResponse, JsonResponse, Http404
from .models import Category, Blank, Bookmark
from .translit import translit
from .forms import FormDownload, UpdateProfileForm, CommentForm


# Create your views here.
@login_required
def categories(request):
    ''' Список всех категорий '''
    categories = Category.objects.order_by('date_added')
    context = {
        'title': 'Категории',
        'categories': categories
    }
    return render(request, 'cabinet/categories.html', context)

@login_required
def category(request, category_id):
    ''' Описание и список всех бланков текущей категории '''
    category = get_object_or_404(Category, id=category_id)
    blanks = category.blank_set.order_by('date_added')
    context = {
        'title': category,
        'category': category,
        'blanks': blanks
    }
    return render(request, 'cabinet/category.html', context)

@login_required
def blank(request, category_id, blank_id):
    ''' Бланк для скачивания '''
    try:
        blank = Blank.objects.filter(category_id=category_id, id=blank_id).get()
    except Blank.DoesNotExist:
        raise Http404
    try:
        bookmark = Bookmark.objects.filter(user=request.user, blank=blank).get()
    except Bookmark.DoesNotExist:
        bookmark = None
        
    form = FormDownload(initial={'title': blank, 'blank': blank.text})
    
    if request.method != 'POST':
        comment_form = CommentForm()
    else:
        comment_form= CommentForm(data=request.POST)
        if comment_form.is_valid():
            author = request.user
            body = comment_form.cleaned_data['body'].strip()
            if len(body) == 0:
                return JsonResponse({'status':'error', 'message': 'Ошибка, заполните данные!'})
            new_comment = blank.comment_set.create(author=author, blank=blank, body=body)
           
            html_comment_add = get_template('cabinet/comment_add.html')
            html_comment_add = html_comment_add.render({'comment': new_comment})
            count = blank.comment_set.count()
            return JsonResponse({
                'status':'success',
                'message': 'Комментарий успешно добавлен!',
                'body': html_comment_add,
                'count': count
                })
        else:
            return JsonResponse({'status':'error', 'message': 'Ошибка, заполните данные!'})
    context = {
        'title': blank,
        'blank': blank,
        'bookmark': bookmark,
        'form': form,
        'comment_form': comment_form
    }
    return render(request, 'cabinet/blank.html', context)

@login_required
def bookmark(request):
    ''' Список закладок '''
    bookmarks = Bookmark.objects.filter(user=request.user)
    context={
        'title': 'Закладки',
        'bookmarks': bookmarks
    }
    return render(request, 'cabinet/bookmark.html', context)

@login_required
def bookmark_add(request):
    ''' Добавить или удалить с закладки '''
    blank_id = request.GET.get('blank_id')
    if blank_id:
        try:
            blank = Blank.objects.get(id=blank_id)
        except Blank.DoesNotExist:
            return JsonResponse({'status': 'error', 'message':'Операция не возможна т.к. нет такой записи в бд.'})

        bookmark_count = Bookmark.objects.filter(user=request.user, blank=blank).count()
        if bookmark_count > 0:
            deleted_bookmark = Bookmark.objects.filter(user=request.user, blank=blank).delete()
            return JsonResponse({
                'status': 'success',
                'method': 'Добавить в закладки',
                'message':'Удалено с закладки: "{}"'.format(blank.title)
            })
        else:
            new_bookmark = Bookmark.objects.create(user=request.user, blank=blank)
            return JsonResponse({
                'status': 'success',
                'method': 'Удалить с закладки',
                'message':'Добавлено в закладки: "{}"'.format(new_bookmark.blank)
            })
           
    return HttpResponse('dd')

@login_required
def download(request):
    ''' Скачать бланк в формате pdf '''
    if request.method == 'POST':
        form = FormDownload(data=request.POST)
        if form.is_valid():
            context = {
                'title': form.cleaned_data['title'],
                'blank': form.cleaned_data['blank'],
            }
            # Получаем документ в html формате
            html_data = get_template('cabinet/download.html')
            html_data = html_data.render(context)
            # Генерируем в pdf формат
            bytes_io = BytesIO()
            pdf_generator = HTML(string=html_data)
            pdf_generator.write_pdf(bytes_io)
            response = HttpResponse(content_type='application/pdf')
            filename = '{}.pdf'.format(translit(context['title']))
            response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
            pdf_data = bytes_io.getvalue()
            bytes_io.close()
            response.write(pdf_data)
            return response
    return HttpResponse('')

@login_required
def profile(request):
    ''' Редактирование профиля '''
    success = ''
    if request.method != 'POST':
        form = UpdateProfileForm(instance=request.user)
    else:
        form = UpdateProfileForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            success = 'Ваш профиль успешно изменен!'
    context = {
        'title': 'Профиль',
        'form': form,
        'success': success
    }
    return render(request, 'cabinet/profile.html', context)
