# blog/filters.py
import django_filters
from django.db.models import Q
from .models import BlogPost, Category, Tag, Author


class BlogPostFilter(django_filters.FilterSet):
    """
    Filter class for BlogPost model with various filtering options
    """
    # Text search across multiple fields
    search = django_filters.CharFilter(method='filter_search', label='Search')

    # Category filtering
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        field_name='category',
        label='Category'
    )
    category__slug = django_filters.CharFilter(
        field_name='category__slug',
        lookup_expr='iexact',
        label='Category Slug'
    )

    # Tag filtering
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags',
        label='Tags'
    )
    tag = django_filters.CharFilter(
        field_name='tags__slug',
        lookup_expr='iexact',
        label='Tag Slug'
    )

    # Author filtering
    author = django_filters.ModelChoiceFilter(
        queryset=Author.objects.all(),
        field_name='author',
        label='Author'
    )
    author__name = django_filters.CharFilter(
        method='filter_author_name',
        label='Author Name'
    )

    # Date filtering
    published_date = django_filters.DateFilter(field_name='published_date')
    published_date__gte = django_filters.DateFilter(
        field_name='published_date',
        lookup_expr='gte',
        label='Published After'
    )
    published_date__lte = django_filters.DateFilter(
        field_name='published_date',
        lookup_expr='lte',
        label='Published Before'
    )
    published_year = django_filters.NumberFilter(
        field_name='published_date__year',
        label='Published Year'
    )
    published_month = django_filters.NumberFilter(
        field_name='published_date__month',
        label='Published Month'
    )

    # Status filtering (for admin/authenticated users)
    status = django_filters.ChoiceFilter(
        choices=BlogPost.STATUS_CHOICES,
        field_name='status',
        label='Status'
    )

    # Featured posts
    is_featured = django_filters.BooleanFilter(
        field_name='is_featured',
        label='Featured Posts Only'
    )

    # Engagement metrics
    views__gte = django_filters.NumberFilter(
        field_name='views',
        lookup_expr='gte',
        label='Minimum Views'
    )
    likes__gte = django_filters.NumberFilter(
        field_name='likes',
        lookup_expr='gte',
        label='Minimum Likes'
    )

    # Reading time
    read_time__gte = django_filters.NumberFilter(
        method='filter_read_time_gte',
        label='Minimum Read Time (minutes)'
    )
    read_time__lte = django_filters.NumberFilter(
        method='filter_read_time_lte',
        label='Maximum Read Time (minutes)'
    )

    class Meta:
        model = BlogPost
        fields = []

    def filter_search(self, queryset, name, value):
        """
        Custom search filter across multiple fields
        """
        if not value:
            return queryset

        return queryset.filter(
            Q(title__icontains=value) |
            Q(excerpt__icontains=value) |
            Q(content__icontains=value) |
            Q(tags__name__icontains=value) |
            Q(category__name__icontains=value) |
            Q(author__user__first_name__icontains=value) |
            Q(author__user__last_name__icontains=value)
        ).distinct()

    def filter_author_name(self, queryset, name, value):
        """
        Filter by author's full name or username
        """
        if not value:
            return queryset

        return queryset.filter(
            Q(author__user__first_name__icontains=value) |
            Q(author__user__last_name__icontains=value) |
            Q(author__user__username__icontains=value)
        ).distinct()

    def filter_read_time_gte(self, queryset, name, value):
        """
        Filter posts with read time greater than or equal to value
        Note: This is an approximation based on content length
        """
        if not value:
            return queryset

        # Approximate word count for filtering
        # Assuming 200 words per minute reading speed
        min_words = int(value) * 200

        # Filter by content length (rough approximation)
        return queryset.extra(
            where=["LENGTH(content) / 5 >= %s"],  # Rough word count estimation
            params=[min_words]
        )

    def filter_read_time_lte(self, queryset, name, value):
        """
        Filter posts with read time less than or equal to value
        """
        if not value:
            return queryset

        max_words = int(value) * 200

        return queryset.extra(
            where=["LENGTH(content) / 5 <= %s"],
            params=[max_words]
        )


class CategoryFilter(django_filters.FilterSet):
    """
    Filter class for Category model
    """
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Category Name'
    )

    class Meta:
        model = Category
        fields = ['name']


class TagFilter(django_filters.FilterSet):
    """
    Filter class for Tag model
    """
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Tag Name'
    )

    class Meta:
        model = Tag
        fields = ['name']


class AuthorFilter(django_filters.FilterSet):
    """
    Filter class for Author model
    """
    name = django_filters.CharFilter(
        method='filter_name',
        label='Author Name'
    )

    class Meta:
        model = Author
        fields = []

    def filter_name(self, queryset, name, value):
        """
        Filter by author's full name or username
        """
        if not value:
            return queryset

        return queryset.filter(
            Q(user__first_name__icontains=value) |
            Q(user__last_name__icontains=value) |
            Q(user__username__icontains=value)
        ).distinct()