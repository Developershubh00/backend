from rest_framework import serializers
from django.utils import timezone
from .models import BlogPost, Category, Tag, Author, BlogPostView, BlogPostLike


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'color_class', 'description']
        read_only_fields = ['slug']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']


class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'avatar', 'website', 'twitter', 'linkedin']


class BlogPostListSerializer(serializers.ModelSerializer):
    """Serializer for blog post list view (minimal data)"""
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    read_time = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'featured_image',
            'author', 'category', 'tags', 'published_date',
            'read_time', 'views', 'likes', 'comments_count',
            'is_featured', 'meta_description'
        ]


class BlogPostDetailSerializer(serializers.ModelSerializer):
    """Serializer for blog post detail view (full data)"""
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    read_time = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'featured_image',
            'author', 'category', 'tags', 'published_date', 'created_at',
            'updated_at', 'read_time', 'views', 'likes', 'comments_count',
            'is_featured', 'meta_description', 'meta_keywords', 'status'
        ]


class BlogPostCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating blog posts"""
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=False
    )
    author_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = BlogPost
        fields = [
            'title', 'excerpt', 'content', 'featured_image',
            'category', 'tags', 'meta_description', 'meta_keywords',
            'is_featured', 'status', 'published_date', 'author_id'
        ]
        extra_kwargs = {
            'published_date': {'required': False},
        }

    def validate_title(self, value):
        """Ensure title is unique for new posts"""
        if self.instance is None:  # Creating new post
            if BlogPost.objects.filter(title=value).exists():
                raise serializers.ValidationError("A post with this title already exists.")
        else:  # Updating existing post
            if BlogPost.objects.filter(title=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("A post with this title already exists.")
        return value

    def validate(self, data):
        """Custom validation"""
        # If status is published, ensure published_date is set
        if data.get('status') == BlogPost.PUBLISHED:
            if not data.get('published_date'):
                data['published_date'] = timezone.now()

        # Validate featured image is provided
        if not data.get('featured_image') and not getattr(self.instance, 'featured_image', None):
            raise serializers.ValidationError({
                'featured_image': 'Featured image is required.'
            })

        return data

    def create(self, validated_data):
        """Create blog post with author"""
        # Set author from request user or provided author_id
        request = self.context.get('request')
        author_id = validated_data.pop('author_id', None)

        if author_id:
            try:
                author = Author.objects.get(id=author_id)
                validated_data['author'] = author
            except Author.DoesNotExist:
                raise serializers.ValidationError({'author_id': 'Invalid author ID.'})
        elif request and hasattr(request.user, 'author'):
            validated_data['author'] = request.user.author
        else:
            raise serializers.ValidationError({'author': 'Author must be specified.'})

        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update blog post"""
        # Handle author update if provided
        author_id = validated_data.pop('author_id', None)
        if author_id:
            try:
                author = Author.objects.get(id=author_id)
                validated_data['author'] = author
            except Author.DoesNotExist:
                raise serializers.ValidationError({'author_id': 'Invalid author ID.'})

        return super().update(instance, validated_data)


class BlogPostAdminSerializer(serializers.ModelSerializer):
    """Full serializer for admin operations"""
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    read_time = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = BlogPost
        fields = '__all__'


class BlogPostViewSerializer(serializers.ModelSerializer):
    """Serializer for tracking post views"""

    class Meta:
        model = BlogPostView
        fields = ['post', 'ip_address', 'user_agent', 'viewed_at']
        read_only_fields = ['viewed_at']


class BlogPostLikeSerializer(serializers.ModelSerializer):
    """Serializer for post likes"""

    class Meta:
        model = BlogPostLike
        fields = ['post', 'ip_address', 'user', 'created_at']
        read_only_fields = ['created_at']


class BlogStatsSerializer(serializers.Serializer):
    """Serializer for blog statistics"""
    total_posts = serializers.IntegerField()
    published_posts = serializers.IntegerField()
    draft_posts = serializers.IntegerField()
    total_views = serializers.IntegerField()
    total_likes = serializers.IntegerField()
    featured_posts = serializers.IntegerField()
    categories_count = serializers.IntegerField()
    tags_count = serializers.IntegerField()
    authors_count = serializers.IntegerField()
    recent_posts = BlogPostListSerializer(many=True)
    popular_posts = BlogPostListSerializer(many=True)