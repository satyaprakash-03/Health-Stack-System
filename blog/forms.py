from django import forms
from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'excerpt', 'content', 'category', 'featured_image', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter blog title...',
                'class': 'blog-input',
            }),
            'excerpt': forms.Textarea(attrs={
                'placeholder': 'Write a short summary (max 500 characters)...',
                'class': 'blog-input',
                'rows': 3,
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your full blog content here...',
                'class': 'blog-input blog-textarea',
                'rows': 14,
            }),
            'category': forms.Select(attrs={
                'class': 'blog-input',
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'blog-checkbox',
            }),
        }
