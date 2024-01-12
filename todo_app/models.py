from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify


class ToDo(models.Model):
    title = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="todo_author")
    slug = models.SlugField(max_length=250, unique=True)
    date_created = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('todo_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Item(models.Model):
    todo = models.ForeignKey(
        ToDo, related_name="items", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)  # Change to a CharField
    slug = models.SlugField(max_length=250, unique=True)
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    due_date = models.DateField(null=True, default=None)

    class Meta:
        ordering = ('due_date', '-date_created')

    def __str__(self):
        return f"{self.title}: due {self.due_date}"

    def get_absolute_url(self): return reverse(
        "item-update", args=[str(self.todo.id), str(self.id)])

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            # Append a timestamp to the slug to ensure uniqueness
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            self.slug = f"{slugify(self.title)}_{timestamp}"
        return super().save(*args, **kwargs)
