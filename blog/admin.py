from django.contrib import admin
from django.contrib.admin import ModelAdmin

from . import models


@admin.register(models.Writer)
class WriterAdmin(ModelAdmin):
    model = models.Writer


@admin.register(models.Article)
class ArticleAdmin(ModelAdmin):
    model = models.Article
