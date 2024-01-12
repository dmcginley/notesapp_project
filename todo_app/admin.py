from django.contrib import admin
from .models import ToDo, Item


@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_created')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date')
    list_filter = ('due_date',)
    date_hierarchy = 'due_date'
