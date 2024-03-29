from django.db import models
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User

from django.utils.text import slugify
from django_quill.fields import QuillField


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True)
    order = models.PositiveIntegerField(default=0)  # Add the order field
    parent_category = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    is_starred = models.BooleanField(default=False)  # field for starred category
    is_deletable = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = "categories"

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.name

    # @classmethod
    # def create(cls, name, is_starred=False, is_deletable=True):
    #     return cls.objects.create(name=name, is_starred=is_starred)

    def delete_category(self):
        if self.is_deletable:
            self.delete()
        else:
            raise Exception("Cannot delete this category")
    def get_absolute_url(self):
        return reverse('board_app:category_list', args=[self.slug])

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         base_slug = slugify(self.name)
    #         slug = base_slug
    #         counter = 1
    #         while Category.objects.filter(slug=slug).exists():
    #             slug = f"{base_slug}-{counter}"
    #             counter += 1
    #         self.slug = slug
    #     super().save(*args, **kwargs)


    @classmethod
    def create(cls, name, is_deletable=True, is_starred=False):
        category = cls(name=name, is_deletable=is_deletable, is_starred=is_starred)
        category.save()  # Call save to generate slug
        return category

if not Category.objects.exists():
    Category.objects.create(name="Projects", is_deletable=True, is_starred=True, order=0)
    Category.objects.create(name="Areas", is_deletable=True, is_starred=True, order=1)
    Category.objects.create(name="Resources", is_deletable=True, is_starred=True, order=2)
    Category.objects.create(name="Archives", is_deletable=True, is_starred=True, order=3)


class Note(models.Model):

    title = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to='note_image')
    content = QuillField(null=True)
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

    def save(self, *args, **kwargs):
        if not self.slug:
            # Create a unique slug based on the title and a timestamp to prevent identical slug
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1

            while Note.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = unique_slug

        super(Note, self).save(*args, **kwargs)
