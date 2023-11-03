from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from django.utils.text import slugify
from django_quill.fields import QuillField


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('board_app:category_list', args=[self.slug])

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Note(models.Model):

    title = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to='note_image')
    content = QuillField(null=True)
    # content = models.TextField(null=True)

    slug = models.SlugField(max_length=250, unique=True)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="note_author")

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('note_detail', kwargs={'slug': self.slug})

    def category_name(self):
        all = []
        for a in self.category.all():
            all.append(str(a))
        return "; ".join(all)

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
