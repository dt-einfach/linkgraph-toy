import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Writer',
            fields=[
                (
                    'deleted',
                    models.DateTimeField(
                        db_index=True, editable=False,
                        null=True,
                    ),
                ),
                ('deleted_by_cascade',
                 models.BooleanField(default=False, editable=False)),
                (
                    'user',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    )
                ),
                ('is_editor', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=120)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'deleted',
                    models.DateTimeField(
                        db_index=True, editable=False, null=True,
                    )
                ),
                (
                    'deleted_by_cascade',
                    models.BooleanField(default=False, editable=False),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                (
                    'status', models.CharField(
                        choices=[
                            ('draft', 'Draft'), ('published', 'Published'),
                            ('archived', 'Archived'),
                        ],
                        default='draft',
                        max_length=10
                    )
                ),
                (
                    'edited_by', models.ForeignKey(
                        blank=True, null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='articles_edited',
                        to='blog.writer'
                    )
                ),
                (
                    'written_by',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='articles_written',
                        to='blog.writer'
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
