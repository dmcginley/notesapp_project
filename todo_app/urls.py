from django.urls import path
from .views import create_item, delete_item

from .views import (
    ToDoListView, ToDoDetailView, ItemsListView
)

urlpatterns = [
    path('', ToDoListView.as_view(), name='todo'),
    path('todo_items/<slug:todo_slug>/',
         ItemsListView.as_view(), name='todo_items'),
    path('todo/<slug:slug>/', ToDoDetailView.as_view(), name='todo_detail'),

    # path('delete/<int:pk>', ItemDeleteView
    #      .as_view(), name='delete_item'),
]


htmxpatterns = [
    # path('create_item/', views.create_item, name='create_item'),

    path('todo/<slug:todo_slug>/create_item/', create_item, name='create_item'),
    path('todo/<slug:todo_slug>/', ToDoDetailView.as_view(), name='todo_detail'),
    path('delete_item/<int:item_pk>/', delete_item, name='delete_item'),
    # path('mark_item/<int:pk>/', views.mark_item, name='mark_item'),
]


urlpatterns += htmxpatterns
