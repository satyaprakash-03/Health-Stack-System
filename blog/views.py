from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import BlogPost
from .forms import BlogPostForm


# ─────────────────────────────────────────
# PUBLIC: Blog List (everyone can view)
# ─────────────────────────────────────────
def blog_list(request):
    search_query  = request.GET.get('search', '')
    category      = request.GET.get('category', '')

    blogs = BlogPost.objects.filter(is_published=True)

    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(content__icontains=search_query)
        )

    if category:
        blogs = blogs.filter(category=category)

    categories = BlogPost.CATEGORY_CHOICES
    context = {
        'blogs': blogs,
        'search_query': search_query,
        'category_filter': category,
        'categories': categories,
        'total': blogs.count(),
    }
    return render(request, 'blog/blog-list.html', context)


# ─────────────────────────────────────────
# PUBLIC: Blog Detail
# ─────────────────────────────────────────
def blog_detail(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug, is_published=True)
    # Increment view count
    blog.views_count += 1
    blog.save(update_fields=['views_count'])

    related = BlogPost.objects.filter(
        category=blog.category, is_published=True
    ).exclude(pk=blog.pk)[:3]

    context = {'blog': blog, 'related': related}
    return render(request, 'blog/blog-detail.html', context)


# ─────────────────────────────────────────
# DOCTOR: Create Blog
# ─────────────────────────────────────────
@login_required(login_url='login')
def blog_create(request):
    if not (request.user.is_authenticated and request.user.is_doctor):
        messages.error(request, 'Only doctors can create blog posts.')
        return redirect('blog-list')

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Blog post created successfully!')
            return redirect('blog-manage')
    else:
        form = BlogPostForm()

    return render(request, 'blog/blog-create.html', {'form': form, 'action': 'Create'})


# ─────────────────────────────────────────
# DOCTOR: Edit Blog
# ─────────────────────────────────────────
@login_required(login_url='login')
def blog_edit(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk, author=request.user)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog updated successfully!')
            return redirect('blog-manage')
    else:
        form = BlogPostForm(instance=blog)

    return render(request, 'blog/blog-create.html', {'form': form, 'action': 'Edit', 'blog': blog})


# ─────────────────────────────────────────
# DOCTOR: Delete Blog
# ─────────────────────────────────────────
@login_required(login_url='login')
def blog_delete(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk, author=request.user)
    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'Blog post deleted.')
    return redirect('blog-manage')


# ─────────────────────────────────────────
# DOCTOR: Toggle Publish
# ─────────────────────────────────────────
@login_required(login_url='login')
def blog_toggle_publish(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk, author=request.user)
    blog.is_published = not blog.is_published
    blog.save(update_fields=['is_published'])
    status = 'published' if blog.is_published else 'unpublished'
    messages.success(request, f'Blog "{blog.title}" is now {status}.')
    return redirect('blog-manage')


# ─────────────────────────────────────────
# DOCTOR: My Blogs Dashboard
# ─────────────────────────────────────────
@login_required(login_url='login')
def blog_manage(request):
    if not (request.user.is_authenticated and request.user.is_doctor):
        messages.error(request, 'Only doctors can manage blog posts.')
        return redirect('blog-list')

    my_blogs = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    published = my_blogs.filter(is_published=True).count()
    drafts    = my_blogs.filter(is_published=False).count()

    context = {
        'my_blogs': my_blogs,
        'published': published,
        'drafts': drafts,
        'total': my_blogs.count(),
    }
    return render(request, 'blog/blog-manage.html', context)
