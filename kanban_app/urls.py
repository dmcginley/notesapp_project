from django.urls import path, include
from . import views


from .views import (
    KanbanListView, ColumnListView
)

app_name = 'kanban_app'

urlpatterns = [
    path('', KanbanListView.as_view(), name='kanban_list'),
    path('column/', ColumnListView.as_view(), name='column_list'),

]
