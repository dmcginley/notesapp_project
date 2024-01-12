from django.http import HttpResponse  # Import if needed
from django.views import View
from django.shortcuts import render, get_object_or_404
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import JsonResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.urls import reverse
from django.urls import reverse_lazy

from django.views.decorators.csrf import csrf_exempt

from .models import ToDo, Item

from django.views.generic import (
    ListView, DetailView
)


class ToDoListView(ListView):
    model = ToDo
    context_object_name = 'todos'  # Use 'todos' for the list of ToDo objects
    template_name = "todo_app/todo.html"

    # def get_queryset(self):
    #     user = self.request.user
    #     return user.todos.all()


class ItemsListView(ListView):
    model = Item
    context_object_name = 'items'
    template_name = "todo_app/todo_items.html"

    def get_queryset(self):
        # Get the todo_slug from the URL
        todo_slug = self.kwargs.get('todo_slug')

        # Get the specific todo list or return 404 if not found
        todo_instance = get_object_or_404(
            ToDo, slug=todo_slug, author=self.request.user)

        # Return the items associated with the todo list
        # return Item.objects.filter(todo=todo_instance)
        items = Item.objects.filter(todo=todo_instance)
        print('items queryset:', items)
        return items


class ToDoDetailView(DetailView):
    model = ToDo
    template_name = "todo_app/todo_items_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['items'] = self.object.items.all()
        return context


@require_POST
def create_item(request, todo_slug):
    title = request.POST.get('itemtitle')

    # Get or create the todo list
    todo_instance = get_object_or_404(
        ToDo, slug=todo_slug, author=request.user)

    if title:
        item = Item.objects.create(
            title=title, todo=todo_instance, user=request.user)

        # Retrieve the correct items associated with the todo
        items = todo_instance.items.all()
        print('all items', items)
        # Render the updated items HTML
        context = {'items': items, 'todo': todo_instance}

        # Return the updated items HTML as the response
        return render(request, 'todo_app/components/todo_items.html', context)


def delete_item(request, todo_slug):
    pass
    # model = Item
    # template_name = 'todo_app/todo_items.html.html'
    # # success_url = '/'

    # def test_func(self):
    #     item = self.get_object()
    #     if self.request.user == item.author:
    #         return True
    #     return False

    # def form_valid(self, form):
    #     messages.success(self.request, 'Item deleted.')
    #     return super().form_valid(form)

    # def get_success_url(self):

    #     # return reverse('post_detail', kwargs={'slug': self.object.post.slug})
    #     return reverse('todo_detail', kwargs={'slug': self.object.todo.slug})


# # Deleting a Todo

# # @csrf_exempt
# def delete_item(request, pk):
#     # pass
#     item = Item.objects.get(pk=pk)
#     item.delete()
#     items = Item.objects.all()

# #     # Render the item list HTML with the CSRF token
#     context = {'items': items}
#     todo_items_html = render_to_string(
#         "todo_app/todo_items.html", context, request=request)

#     data = {
#         'todo_items_html': todo_items_html,
#         'csrf_token': request.META.get('CSRF_COOKIE')
#     }

#     # return JsonResponse(data)
#     return render(request, 'todo_app/todo_items.html', {'items': items})
