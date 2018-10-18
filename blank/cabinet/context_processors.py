from django.core.urlresolvers import resolve, Resolver404
from .models import Category

def nav_categories(request):
    try:
        current_url = resolve(request.path_info).url_name
    except Resolver404:
        return {}
    if current_url == 'index' or current_url == 'categories'\
        or current_url == 'category' or current_url == 'blank' \
        or current_url == 'profile' or current_url == 'account_logout'\
        or current_url == 'bookmark':
        categories = Category.objects.all()
        category_id = int(request.resolver_match.kwargs.get('category_id', 0))
        context_data = {
            'nav_categories': categories,
            'category_id': category_id
        }
        return context_data
    return {}
