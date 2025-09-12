# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Blog posts
    path('', views.BlogPostListView.as_view(), name='post_list'),
    path('create/', views.BlogPostCreateView.as_view(), name='post_create'),
    path('featured/', views.FeaturedPostsView.as_view(), name='featured_posts'),
    path('stats/', views.blog_stats, name='blog_stats'),
    path('search/', views.search_posts, name='search_posts'),

    # Blog post detail, update, delete
    path('<slug:slug>/', views.BlogPostDetailView.as_view(), name='post_detail'),
    path('<slug:slug>/edit/', views.BlogPostUpdateView.as_view(), name='post_update'),
    path('<slug:slug>/delete/', views.BlogPostDeleteView.as_view(), name='post_delete'),
    path('<slug:slug>/like/', views.like_post, name='like_post'),
    path('<slug:slug>/related/', views.related_posts, name='related_posts'),

    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),

    # Tags
    path('tags/', views.TagListView.as_view(), name='tag_list'),

    # Authors
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
]