from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.


class Board(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="board_author")
    name = models.CharField(max_length=100, unique=True)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        verbose_name_plural = "boards"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('board_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Column(models.Model):
    authors = models.ManyToManyField(
        User, related_name="columns")
    board = models.ForeignKey(
        Board, related_name="columns", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    # slug = models.SlugField(max_length=250, unique=True)
    order = models.PositiveIntegerField()  # Add the order field

    class Meta:
        verbose_name_plural = "columns"

    # def save(self, *args, **kwargs):  # new
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     return super().save(*args, **kwargs)


class Task(models.Model):
    users = models.ManyToManyField(User, related_name="boards")
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    # slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        ordering = ('-date_created',)

    # def save(self, *args, **kwargs):  # new
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     return super().save(*args, **kwargs)


class UserColumns(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ('order',)
