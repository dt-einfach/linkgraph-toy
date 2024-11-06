from django.conf import settings
from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel


class Writer(SafeDeleteModel):
    """
    Writer model class.
    """
    _safedelete_policy = SOFT_DELETE_CASCADE

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='writer',
    )
    is_editor = models.BooleanField(default=False)
    name = models.CharField(max_length=120)

    objects = models.Manager()

    def __str__(self):
        return f"Writer {self.name}"


class Article(SafeDeleteModel):
    """
    Article model class.
    """
    _safedelete_policy = SOFT_DELETE_CASCADE

    DRAFT = 'draft'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
        (ARCHIVED, 'Archived'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=DRAFT,
    )
    written_by = models.ForeignKey(
        Writer,
        on_delete=models.CASCADE,
        related_name='articles_written',
    )
    edited_by = models.ForeignKey(
        Writer,
        on_delete=models.CASCADE,
        related_name='articles_edited',
        null=True,
        blank=True,
    )

    objects = models.Manager()

    def __str__(self):
        return f"Article {self.title}"
