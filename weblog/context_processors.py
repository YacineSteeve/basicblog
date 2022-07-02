from .models import BlogPost, Comment, Category


def top_categories(request):
    categories = []
    blog_posts = BlogPost.objects.all()

    for category in Category.objects.all():
        count = 0
        for blog_post in blog_posts:
            if category in blog_post.categories.all():
                count += 1
        if count != 0:
            categories.append((category, count))

    categories = categories[:10]

    return {'top_categories': sorted(categories, key=lambda x: x[1], reverse=True)}


def popular_content(request):
    blogposts = []

    for blogpost in BlogPost.objects.all():
        count = blogpost.get_comments_number()
        if count != 0:
            blogposts.append((blogpost, count, blogpost.id))

    blogposts = blogposts[:10]

    return {'popular_content': sorted(blogposts, key=lambda x: x[1], reverse=True)}
