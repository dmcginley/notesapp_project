from django.contrib import admin
from .models import Board, Task, Column

# Register your models here.


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name', 'board')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'column')
