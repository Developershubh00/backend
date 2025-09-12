from django.shortcuts import render

# Create your views here.
# blog/views.py
from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Sum
from django.utils import timezone
from django.core.cache import cache

from .models import BlogPost, Category, Tag, Author, BlogPostView, BlogPostLike
from .serializers import (
    BlogPostListSerializer, BlogPostDetailSerializer,
    BlogPostCreateUpdateSerializer, CategorySerializer,
    TagSerializer, AuthorSerializer, BlogStatsSerializer,
    BlogPostViewSerializer, BlogPostLikeSerializer
)
from .filters import BlogPostFilter
from .permissions import IsAuthorOrReadOnly


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class BlogPostListView(generics.ListAPIView):
    """
    List all published blog posts with pagination, search, and filtering
    """
    serializer_class = BlogPostListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BlogPostFilter
    search_fields = ['title', 'excerpt', 'content', 'tags__name', 'category__name']
    ordering_fields = ['published_date', 'views', 'likes', 'created_at']
    ordering = ['-published_date']

    def get_queryset(self):
        return BlogPost.objects.filter(
            status=BlogPost.PUBLISHED,
            published_date__lte=timezone.now()
        ).select_related(
            'author', 'author__user', 'category'
        ).prefetch_related(
            'tags'
        )


class BlogPostDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single blog post by slug and increment view count
    """
    serializer_class = BlogPostDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return BlogPost.objects.filter(
            status=BlogPost.PUBLISHED
        ).select_related(
            'author', 'author__user', 'category'
        ).prefetch_related(
            'tags'
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Track view if not already viewed by this IP
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        view_obj, created = BlogPostView.objects.get_or_create(
            post=instance,
            ip_address=ip_address,
            defaults={'user_agent': user_agent}
        )

        if created:
            # Increment view count on post
            instance.views += 1
            instance.save(update_fields=['views'])

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BlogPostCreateView(generics.CreateAPIView):
    """
    Create a new blog post (authenticated users only)
    """
    serializer_class = BlogPostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Ensure user has an author profile
        author, created = Author.objects.get_or_create(
            user=self.request.user,
            defaults={'bio': ''}
        )
        serializer.save(author=author)


class BlogPostUpdateView(generics.UpdateAPIView):
    """
    Update a blog post (author or admin only)
    """
    serializer_class = BlogPostCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    lookup_field = 'slug'

    def get_queryset(self):
        return BlogPost.objects.all()


class BlogPostDeleteView(generics.DestroyAPIView):
    """
    Delete a blog post (author or admin only)
    """
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    lookup_field = 'slug'

    def get_queryset(self):
        return BlogPost.objects.all()


class FeaturedPostsView(generics.ListAPIView):
    """
    List featured blog posts
    """
    serializer_class = BlogPostListSerializer

    def get_queryset(self):
        return BlogPost.objects.filter(
            status=BlogPost.PUBLISHED,
            is_featured=True,
            published_date__lte=timezone.now()
        ).select_related(
            'author', 'author__user', 'category'
        ).prefetch_related(
            'tags'
        ).order_by('-published_date')[:5]


class CategoryListView(generics.ListAPIView):
    """
    List all categories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveAPIView):
    """
    Get category details with related posts
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class TagListView(generics.ListAPIView):
    """
    List all tags
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class AuthorListView(generics.ListAPIView):
    """
    List all authors
    """
    queryset = Author.objects.all().select_related('user')
    serializer_class = AuthorSerializer


class AuthorDetailView(generics.RetrieveAPIView):
    """
    Get author details
    """
    queryset = Author.objects.all().select_related('user')
    serializer_class = AuthorSerializer


@api_view(['POST'])
@permission_classes([])
def like_post(request, slug):
    """
    Like/unlike a blog post
    """
    try:
        post = BlogPost.objects.get(slug=slug, status=BlogPost.PUBLISHED)
    except BlogPost.DoesNotExist:
        return Response(
            {'error': 'Post not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    ip_address = get_client_ip(request)
    user = request.user if request.user.is_authenticated else None

    # Check if already liked
    like_obj = BlogPostLike.objects.filter(
        post=post,
        ip_address=ip_address
    ).first()

    if like_obj:
        # Unlike the post
        like_obj.delete()
        post.likes = max(0, post.likes - 1)
        liked = False
    else:
        # Like the post
        BlogPostLike.objects.create(
            post=post,
            ip_address=ip_address,
            user=user
        )
        post.likes += 1
        liked = True

    post.save(update_fields=['likes'])

    return Response({
        'liked': liked,
        'likes_count': post.likes
    })


@api_view(['GET'])
def blog_stats(request):
    """
    Get blog statistics
    """
    cache_key = 'blog_stats'
    stats = cache.get(cache_key)

    if not stats:
        # Calculate stats
        total_posts = BlogPost.objects.count()
        published_posts = BlogPost.objects.filter(status=BlogPost.PUBLISHED).count()
        draft_posts = BlogPost.objects.filter(status=BlogPost.DRAFT).count()
        total_views = BlogPost.objects.aggregate(
            total=Sum('views')
        )['total'] or 0
        total_likes = BlogPost.objects.aggregate(
            total=Sum('likes')
        )['total'] or 0
        featured_posts = BlogPost.objects.filter(is_featured=True).count()
        categories_count = Category.objects.count()
        tags_count = Tag.objects.count()
        authors_count = Author.objects.count()

        # Recent posts (last 5)
        recent_posts = BlogPost.objects.filter(
            status=BlogPost.PUBLISHED
        ).select_related(
            'author', 'category'
        ).prefetch_related(
            'tags'
        ).order_by('-published_date')[:5]

        # Popular posts (top 5 by views)
        popular_posts = BlogPost.objects.filter(
            status=BlogPost.PUBLISHED
        ).select_related(
            'author', 'category'
        ).prefetch_related(
            'tags'
        ).order_by('-views')[:5]

        stats = {
            'total_posts': total_posts,
            'published_posts': published_posts,
            'draft_posts': draft_posts,
            'total_views': total_views,
            'total_likes': total_likes,
            'featured_posts': featured_posts,
            'categories_count': categories_count,
            'tags_count': tags_count,
            'authors_count': authors_count,
            'recent_posts': BlogPostListSerializer(recent_posts, many=True).data,
            'popular_posts': BlogPostListSerializer(popular_posts, many=True).data,
        }

        # Cache for 1 hour
        cache.set(cache_key, stats, 3600)

    serializer = BlogStatsSerializer(data=stats)
    serializer.is_valid()
    return Response(serializer.validated_data)


@api_view(['GET'])
def search_posts(request):
    """
    Advanced search for blog posts
    """
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    tag = request.GET.get('tag', '')
    author = request.GET.get('author', '')

    if not query and not category and not tag and not author:
        return Response({'results': []})

    posts = BlogPost.objects.filter(status=BlogPost.PUBLISHED)

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        )

    if category:
        posts = posts.filter(category__slug=category)

    if tag:
        posts = posts.filter(tags__slug=tag)

    if author:
        posts = posts.filter(author__id=author)

    posts = posts.select_related(
        'author', 'category'
    ).prefetch_related('tags').distinct().order_by('-published_date')

    serializer = BlogPostListSerializer(posts, many=True)
    return Response({'results': serializer.data})


@api_view(['GET'])
def related_posts(request, slug):
    """
    Get related posts based on category and tags
    """
    try:
        post = BlogPost.objects.get(slug=slug, status=BlogPost.PUBLISHED)
    except BlogPost.DoesNotExist:
        return Response(
            {'error': 'Post not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Find related posts by category and tags
    related = BlogPost.objects.filter(
        status=BlogPost.PUBLISHED
    ).exclude(
        id=post.id
    ).filter(
        Q(category=post.category) | Q(tags__in=post.tags.all())
    ).select_related(
        'author', 'category'
    ).prefetch_related(
        'tags'
    ).distinct().order_by('-published_date')[:5]

    serializer = BlogPostListSerializer(related, many=True)
    return Response({'results': serializer.data})