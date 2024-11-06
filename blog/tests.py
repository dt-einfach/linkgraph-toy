from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Writer, Article


class WriterArticleTestCase(TestCase):
    def setUp(self):

        # users:
        self.user_writer = User.objects.create_user(
            username='writer', password='password',
        )
        self.user_editor = User.objects.create_user(
            username='editor', password='password',
        )
        self.user_non_writer = User.objects.create_user(
            username='non_writer', password='password',
        )

        # writers:
        self.writer = Writer.objects.create(
            user=self.user_writer, name='writer name', is_editor=False,
        )
        self.editor = Writer.objects.create(
            user=self.user_editor, name='editor name', is_editor=True,
        )

        self.client = APIClient()

    def test_writer_can_create_article(self):
        self.client.login(username='writer', password='password')

        data = {
            'title': 'test article',
            'content': 'test article content',
        }

        response = self.client.post(reverse('blog-article-creation'), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Article.objects.count(), 1)
        article = Article.objects.first()
        self.assertEqual(article.title, 'test article')
        self.assertEqual(article.written_by, self.writer)

    def test_non_writer_cannot_create_article(self):
        self.client.login(username='non_writer', password='password')

        data = {
            'title': 'test article',
            'content': 'test article content',
        }

        response = self.client.post(reverse('blog-article-creation'), data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Article.objects.count(), 0)

    def test_editor_can_approve_article(self):
        article = Article.objects.create(
            title='test article',
            content='test article content',
            written_by=self.writer,
            status=Article.DRAFT,
        )

        self.client.login(username='editor', password='password')

        data = {
            'status': Article.PUBLISHED,
        }

        response = self.client.patch(
            reverse('blog-article-approval-id', args=[article.id]),
            data,
        )
        self.assertEqual(response.status_code, 200)
        article.refresh_from_db()
        self.assertEqual(article.status, Article.PUBLISHED)
        self.assertEqual(article.edited_by, self.editor)

    def test_non_editor_cannot_approve_article(self):
        article = Article.objects.create(
            title='test article',
            content='test article content',
            written_by=self.writer,
            status=Article.DRAFT,
        )

        self.client.login(username='writer', password='password')

        data = {
            'status': Article.PUBLISHED,
        }

        response = self.client.patch(
            reverse('blog-article-approval-id', args=[article.id]),
            data,
        )
        self.assertEqual(response.status_code, 403)
        article.refresh_from_db()
        self.assertEqual(article.status, Article.DRAFT)
        self.assertIsNone(article.edited_by)
