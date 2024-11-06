from datetime import timedelta

from django.db.models import Count, Q, F
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import Article
from .tools import mixins
from .tools.write import get_writer_obj


class DashboardView(View):

    def get(self, request):
        date_30_days_ago = timezone.now() - timedelta(days=30)
        articles = (
            Article.objects
            .annotate(writer=F('written_by__name'))
            .values('writer')
            .annotate(
                total_art_written=Count('id'),
                total_art_written_last_30_d=Count(
                    'id',
                    filter=Q(created_at__gte=date_30_days_ago)
                )
            )
            .order_by()
        )
        ctx = {
            'request': request,
            'writers_summary': list(articles),
        }
        return render(request, 'blog/dashboard.html', ctx)


class ArticleCreationView(mixins.IsWriterMixin, APIView):

    def get(self, request):
        return render(request, "blog/new_article.html")

    def post(self, request):
        data = request.data.copy()
        data['written_by'] = get_writer_obj(request.user)
        data['status'] = Article.DRAFT

        serializer = serializers.ArticleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleView(mixins.IsWriterMixin, APIView):

    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        ctx = {
            'request': request,
            'article': serializers.ArticleDetailSerializer(
                article,
                context={'request': request},
            ).data,
        }
        return render(request, 'blog/article.html', ctx)

    def put(self, request, article_id):
        data = request.data.copy()
        data['written_by'] = get_writer_obj(request.user)

        article = get_object_or_404(Article, id=article_id)
        serializer = serializers.ArticleSerializer(article, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleApprovalView(mixins.IsEditorMixin, APIView):

    def get(self, request):
        articles = Article.objects.filter(status='draft')
        ctx = {
            'request': request,
            'articles': serializers.ArticleSerializer(
                articles,
                context={'request': request},
                many=True,
            ).data,
        }
        return render(request, 'blog/article-approval.html', ctx)

    def patch(self, request, article_id):
        data = request.data.copy()
        data['edited_by'] = get_writer_obj(request.user)

        article = get_object_or_404(Article, id=article_id)
        serializer = serializers.ArticleStatusUpdateSerializer(
            article,
            data=data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleEditedView(mixins.IsEditorMixin, APIView):

    def get(self, request):
        articles = Article.objects.filter(edited_by__pk=request.user.pk)
        ctx = {
            'request': request,
            'articles': serializers.ArticleSerializer(
                articles, context={'request': request}, many=True,
            ).data,
        }
        return render(request, 'blog/article-edited.html', ctx)
