# blog/management/commands/create_sample_blog_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import BlogPost, Category, Tag, Author
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Create sample blog data for testing'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'NEET PG', 'color_class': 'bg-blue-100 text-blue-800', 'description': 'NEET PG related posts'},
            {'name': 'NEET UG', 'color_class': 'bg-red-100 text-red-800', 'description': 'NEET UG related posts'},
            {'name': 'Counselling', 'color_class': 'bg-purple-100 text-purple-800',
             'description': 'Medical admission counselling'},
            {'name': 'Finance', 'color_class': 'bg-green-100 text-green-800',
             'description': 'Medical education finance'},
            {'name': 'Analysis', 'color_class': 'bg-orange-100 text-orange-800',
             'description': 'Data analysis and trends'},
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories.append(category)
            if created:
                self.stdout.write(f"Created category: {category.name}")

        # Create tags
        tags_data = [
            'NEET PG', 'NEET UG', 'Counselling', 'Medical Admission', 'Finance',
            'Fees', 'Government Colleges', 'Private Colleges', 'Cutoff',
            'Analysis', 'State Quota', 'AIQ', 'Rankings', 'Planning', 'Tips'
        ]

        tags = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
            if created:
                self.stdout.write(f"Created tag: {tag.name}")

        # Create or get admin user for author
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Blog',
                'last_name': 'Admin',
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()

        # Create author profile
        author, created = Author.objects.get_or_create(
            user=admin_user,
            defaults={
                'bio': 'Expert medical education consultant with years of experience in NEET guidance.'
            }
        )

        # Sample blog posts data
        posts_data = [
            {
                'title': 'NEET PG 2025: Complete Guide to Counselling Process',
                'excerpt': 'Everything you need to know about NEET PG 2025 counselling including registration dates, document verification, and seat allotment.',
                'content': '''
                <h2>NEET PG 2025 Counselling Overview</h2>
                <p>The NEET PG 2025 counselling is a crucial phase for medical graduates seeking admission to postgraduate courses. With thousands of seats across various specialties, understanding the complete process is essential.</p>

                <h3>Important Dates</h3>
                <ul>
                    <li>Registration: March 2025</li>
                    <li>Choice Filling: April 2025</li>
                    <li>Seat Allotment: May 2025</li>
                </ul>

                <h3>Required Documents</h3>
                <p>Ensure you have all necessary documents ready for the counselling process...</p>
                ''',
                'category': categories[0],  # NEET PG
                'tags': [tags[0], tags[2], tags[3]],  # NEET PG, Counselling, Medical Admission
                'is_featured': True,
            },
            {
                'title': 'Medical College Fee Structure: Complete Breakdown 2025',
                'excerpt': 'Comprehensive analysis of fee structures across government, private, and deemed medical colleges.',
                'content': '''
                <h2>Understanding Medical College Fees</h2>
                <p>Medical education costs vary significantly across different types of institutions. Here's a detailed breakdown...</p>

                <h3>Government Medical Colleges</h3>
                <p>Government colleges offer the most affordable option with fees ranging from ₹20,000 to ₹1,00,000 per year.</p>

                <h3>Private Medical Colleges</h3>
                <p>Private institutions typically charge between ₹10,00,000 to ₹25,00,000 per year.</p>
                ''',
                'category': categories[3],  # Finance
                'tags': [tags[4], tags[5], tags[14]],  # Finance, Fees, Planning
                'is_featured': False,
            },
        ]

        # Create blog posts
        for i, post_data in enumerate(posts_data):
            # Remove tags from post_data for creation
            post_tags = post_data.pop('tags')

            # Set publish date
            post_data['published_date'] = timezone.now() - timedelta(days=i * 2)
            post_data['status'] = BlogPost.PUBLISHED
            post_data['author'] = author

            post, created = BlogPost.objects.get_or_create(
                title=post_data['title'],
                defaults=post_data
            )

            if created:
                # Add tags to the post
                post.tags.set(post_tags)
                self.stdout.write(f"Created blog post: {post.title}")

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample blog data!')
        )