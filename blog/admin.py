# blog/admin.py
from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import BlogPost, Category, Tag, Author, BlogPostView, BlogPostLike


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'posts_count', 'color_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            posts_count=Count('blog_posts')
        )

    def posts_count(self, obj):
        count = obj.posts_count
        if count > 0:
            url = reverse('admin:blog_blogpost_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} posts</a>', url, count)
        return '0 posts'

    posts_count.short_description = 'Posts'
    posts_count.admin_order_field = 'posts_count'

    def color_preview(self, obj):
        return format_html(
            '<span class="badge" style="background-color: #e0e7ff; color: #3730a3; padding: 4px 8px; border-radius: 12px;">{}</span>',
            obj.color_class
        )

    color_preview.short_description = 'Color Class'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'posts_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            posts_count=Count('blog_posts')
        )

    def posts_count(self, obj):
        count = obj.posts_count
        if count > 0:
            url = reverse('admin:blog_blogpost_changelist') + f'?tags__id__exact={obj.id}'
            return format_html('<a href="{}">{} posts</a>', url, count)
        return '0 posts'

    posts_count.short_description = 'Posts'
    posts_count.admin_order_field = 'posts_count'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'posts_count', 'avatar_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'bio']
    readonly_fields = ['created_at', 'updated_at', 'avatar_preview']
    raw_id_fields = ['user']

    fieldsets = (
        (None, {
            'fields': ('user', 'bio')
        }),
        ('Media', {
            'fields': ('avatar', 'avatar_preview')
        }),
        ('Social Links', {
            'fields': ('website', 'twitter', 'linkedin'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').annotate(
            posts_count=Count('blog_posts')
        )

    def posts_count(self, obj):
        count = obj.posts_count
        if count > 0:
            url = reverse('admin:blog_blogpost_changelist') + f'?author__id__exact={obj.id}'
            return format_html('<a href="{}">{} posts</a>', url, count)
        return '0 posts'

    posts_count.short_description = 'Posts'
    posts_count.admin_order_field = 'posts_count'

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" />',
                obj.avatar.url
            )
        return 'No avatar'

    avatar_preview.short_description = 'Avatar Preview'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'author', 'category', 'status', 'is_featured',
        'views', 'likes', 'published_date', 'created_at'
    ]
    list_filter = [
        'status', 'is_featured', 'category', 'published_date',
        'created_at', 'author'
    ]
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    readonly_fields = [
        'slug', 'views', 'likes', 'read_time', 'comments_count',
        'created_at', 'updated_at', 'featured_image_preview'
    ]
    raw_id_fields = ['author']
    date_hierarchy = 'published_date'

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title', 'slug', 'author', 'status', 'is_featured'
            )
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image', 'featured_image_preview')
        }),
        ('Classification', {
            'fields': ('category', 'tags'),
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('published_date',),
        }),
        ('Statistics', {
            'fields': ('views', 'likes', 'read_time', 'comments_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'author', 'author__user', 'category'
        ).prefetch_related('tags')

    def featured_image_preview(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="width: 200px; height: auto; border-radius: 8px;" />',
                obj.featured_image.url
            )
        return 'No image'

    featured_image_preview.short_description = 'Image Preview'

    actions = ['make_featured', 'remove_featured', 'publish_posts', 'draft_posts']

    def make_featured(self, request, queryset):
        count = queryset.update(is_featured=True)
        self.message_user(
            request,
            f'{count} posts were marked as featured.'
        )

    make_featured.short_description = 'Mark selected posts as featured'

    def remove_featured(self, request, queryset):
        count = queryset.update(is_featured=False)
        self.message_user(
            request,
            f'{count} posts were removed from featured.'
        )

    remove_featured.short_description = 'Remove featured status'

    def publish_posts(self, request, queryset):
        from django.utils import timezone
        count = queryset.update(
            status=BlogPost.PUBLISHED,
            published_date=timezone.now()
        )
        self.message_user(
            request,
            f'{count} posts were published.'
        )

    publish_posts.short_description = 'Publish selected posts'

    def draft_posts(self, request, queryset):
        count = queryset.update(status=BlogPost.DRAFT)
        self.message_user(
            request,
            f'{count} posts were moved to draft.'
        )

    draft_posts.short_description = 'Move to draft'


@admin.register(BlogPostView)
class BlogPostViewAdmin(admin.ModelAdmin):
    list_display = ['post', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['post__title', 'ip_address']
    readonly_fields = ['post', 'ip_address', 'user_agent', 'viewed_at']

    def has_add_permission(self, request):
        return False  # Don't allow manual creation

    def has_change_permission(self, request, obj=None):
        return False  # Don't allow editing


@admin.register(BlogPostLike)
class BlogPostLikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'ip_address', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['post__title', 'ip_address', 'user__username']
    readonly_fields = ['post', 'ip_address', 'user', 'created_at']

    def has_add_permission(self, request):
        return False  # Don't allow manual creation

    def has_change_permission(self, request, obj=None):
        return False  # Don't allow editing