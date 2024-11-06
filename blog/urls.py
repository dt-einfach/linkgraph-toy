from django.urls import path

from . import views

urlpatterns = [
    path(
        'article/<article_id>/', views.ArticleView.as_view(),
        name='blog-article-id',
    ),
    path('article/', views.ArticleView.as_view(), name='blog-article'),
    path(
        'article-creation/', views.ArticleCreationView.as_view(),
        name='blog-article-creation',
    ),
    path(
        'article-approval/', views.ArticleApprovalView.as_view(),
        name='blog-article-approval',
    ),
    path(
        'article-approval/<article_id>/', views.ArticleApprovalView.as_view(),
        name='blog-article-approval-id',
    ),
    path(
        'article-edited/', views.ArticleEditedView.as_view(),
        name='blog-article-edited',
    ),
    path('', views.DashboardView.as_view(), name='blog-dashboard'),
]
