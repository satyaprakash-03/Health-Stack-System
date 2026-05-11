from django.db import models
from django.utils.text import slugify
from django.conf import settings


class BlogPost(models.Model):

    CATEGORY_CHOICES = [
        ('fever', 'Fever & Temperature'),
        ('pain', 'Pain Relief'),
        ('cough', 'Cough & Cold'),
        ('diabetes', 'Diabetes Care'),
        ('bloodpressure', 'Blood Pressure'),
        ('heartdisease', 'Heart Disease'),
        ('vitamins', 'Vitamins & Supplements'),
        ('allergy', 'Allergy'),
        ('asthma', 'Asthma'),
        ('digestivehealth', 'Digestive Health'),
        ('skin', 'Skin Care'),
        ('mentalhealth', 'Mental Health'),
        ('nutrition', 'Nutrition & Diet'),
        ('fitness', 'Fitness & Exercise'),
        ('firstaid', 'First Aid'),
        ('general', 'General Health'),
    ]

    title           = models.CharField(max_length=300)
    slug            = models.SlugField(max_length=350, unique=True, blank=True)
    excerpt         = models.TextField(max_length=500, help_text="Short summary shown in listing")
    content         = models.TextField()
    featured_image  = models.ImageField(upload_to='blog/', null=True, blank=True)
    category        = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='general')
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    is_published    = models.BooleanField(default=False)
    views_count     = models.PositiveIntegerField(default=0)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_category_display_name(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, 'General Health')
