# blog/signals.py
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.contrib.auth.models import User
from .models import BlogPost, Author, BlogPostView, BlogPostLike
import os


@receiver(post_save, sender=User)
def create_author_profile(sender, instance, created, **kwargs):
    """
    Automatically create an Author profile when a User is created
    """
    if created:
        Author.objects.get_or_create(
            user=instance,
            defaults={'bio': ''}
        )


@receiver(post_save, sender=BlogPost)
def clear_blog_cache_on_post_save(sender, instance, **kwargs):
    """
    Clear blog-related cache when a post is saved
    """
    cache_keys = [
        'blog_stats',
        f'featured_posts',
        f'recent_posts',
        f'popular_posts'
    ]

    for key in cache_keys:
        cache.delete(key)


@receiver(pre_delete, sender=BlogPost)
def delete_blog_images(sender, instance, **kwargs):
    """
    Delete associated images when a blog post is deleted
    """
    if instance.featured_image:
        if os.path.isfile(instance.featured_image.path):
            os.remove(instance.featured_image.path)


@receiver(pre_delete, sender=Author)
def delete_author_avatar(sender, instance, **kwargs):
    """
    Delete author avatar when author is deleted
    """
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)


@receiver(post_save, sender=BlogPostView)
def update_post_views_count(sender, instance, created, **kwargs):
    """
    Update post views count when a new view is created
    """
    if created:
        # Clear blog stats cache
        cache.delete('blog_stats')


@receiver(post_save, sender=BlogPostLike)
@receiver(pre_delete, sender=BlogPostLike)
def update_post_likes_count(sender, instance, **kwargs):
    """
    Update post likes count when likes are added/removed
    """
    # Clear blog stats cache
    cache.delete('blog_stats')