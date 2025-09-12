from django.db import models

# Create your models here.
from django.contrib import admin

# Register your models here.
# blog/models.py
from django.db import models

from django.utils.text import slugify
from django.urls import reverse
from PIL import Image
import os

# blog/models.py
from django.conf import settings   # ✅ use settings.AUTH_USER_MODEL
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from PIL import Image
import os



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    color_class = models.CharField(
        max_length=100,
        default='bg-gray-100 text-gray-800',
        help_text='Tailwind CSS classes for styling'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Author(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,   # instead of User
        on_delete=models.CASCADE,
        related_name="author_profile"
    )
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(
        upload_to='authors/avatars/',
        blank=True,
        null=True,
        help_text='Author profile picture'
    )
    website = models.URLField(blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Resize avatar image
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                img.thumbnail((300, 300))
                img.save(self.avatar.path)

    @property
    def name(self):
        return self.user.get_full_name() or self.user.username

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'

    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
        (ARCHIVED, 'Archived'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    excerpt = models.TextField(
        max_length=500,
        help_text='Brief description of the blog post'
    )
    content = models.TextField()
    featured_image = models.ImageField(
        upload_to='blog/images/',
        help_text='Main image for the blog post'
    )

    # Relationships
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='blog_posts')

    # Meta fields
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text='SEO meta description'
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text='SEO meta keywords (comma separated)'
    )

    # Status and visibility
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=DRAFT
    )
    is_featured = models.BooleanField(
        default=False,
        help_text='Feature this post on homepage'
    )

    # Engagement metrics
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)

    # Timestamps
    published_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date', '-created_at']
        indexes = [
            models.Index(fields=['status', 'published_date']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['is_featured', 'status']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        # Auto-generate meta description if empty
        if not self.meta_description:
            self.meta_description = self.excerpt[:160]

        # Set published_date when status changes to published
        if self.status == self.PUBLISHED and not self.published_date:
            from django.utils import timezone
            self.published_date = timezone.now()

        super().save(*args, **kwargs)

        # Resize featured image
        if self.featured_image:
            img = Image.open(self.featured_image.path)
            if img.height > 600 or img.width > 800:
                img.thumbnail((800, 600))
                img.save(self.featured_image.path)

    @property
    def read_time(self):
        """Calculate estimated read time in minutes"""
        word_count = len(self.content.split())
        return max(1, round(word_count / 200))  # Assuming 200 words per minute

    @property
    def comments_count(self):
        """Get comment count - placeholder for future comment system"""
        return getattr(self, '_comments_count', 0)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def increment_views(self):
        """Increment view count"""
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title


class BlogPostView(models.Model):
    """Track unique views per IP/session"""
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='post_views'
    )
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['post', 'ip_address']
        indexes = [
            models.Index(fields=['post', 'ip_address']),
        ]

    def __str__(self):
        return f"{self.post.title} - {self.ip_address}"


class BlogPostLike(models.Model):
    """Track likes per IP/user"""
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='post_likes'
    )
    ip_address = models.GenericIPAddressField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # instead of User
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['post', 'ip_address']
        indexes = [
            models.Index(fields=['post', 'ip_address']),
        ]

    def __str__(self):
        return f"Like for {self.post.title}"