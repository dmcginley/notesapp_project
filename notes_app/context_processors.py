# Replace 'yourapp' with the actual app name
from notes_app.models import Category


def starred_categories(request):
    starred_categories = Category.objects.filter(is_starred=True)
    return {'starred_categories': starred_categories}
