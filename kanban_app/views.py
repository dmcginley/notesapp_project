
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect

from .models import Board, Column, Task, UserColumns

from django.views.generic import (
    ListView,
)


# --------------------------------
#   note views
# --------------------------------
class KanbanListView(ListView):
    """ The homepage """
    model = Board
    context_object_name = 'boards'
    # paginate_by = 6
    template_name = "kanban_app/kanban.html"


class ColumnListView(ListView):
    model = Column
    context_object_name = 'columns'
    template_name = "kanban_app/column_list.html"
