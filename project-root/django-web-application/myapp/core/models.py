from django.db import models
from django.core.validators import MinValueValidator
 
 
class User(models.Model):
    """GitHub user / repo owner."""
    username = models.CharField(max_length=200, unique=True)
 
    class Meta:
        ordering = ['username']
 
    def __str__(self):
        return self.username
 
 
class Language(models.Model):
    """Programming language. Normalized so we can group by it in analytics."""
    name = models.CharField(max_length=100, unique=True)
 
    class Meta:
        ordering = ['name']
 
    def __str__(self):
        return self.name
 
 
class Repository(models.Model):
    """A GitHub repository. Belongs to a User, has a Language."""
 
    SOURCE_CHOICES = [
        ('csv', 'CSV Import'),
        ('api', 'GitHub API'),
    ]
 
    repo_name = models.CharField(max_length=1000)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='repos',
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='repos',
    )
    stars = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    url = models.URLField(max_length=1000)
    created_at = models.DateField(null=True, blank=True)
    source = models.CharField(
        max_length=10,
        choices=SOURCE_CHOICES,
        default='csv',
    )
    fetched_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = ['-stars']
        unique_together = ['repo_name', 'owner']
        verbose_name_plural = 'Repositories'
 
    def __str__(self):
        return f"{self.owner.username}/{self.repo_name} ({self.stars}⭐)"

class NbaStat(models.Model):
    player = models.CharField(max_length=100)
    year = models.IntegerField()
    pts = models.FloatField()
    eff = models.FloatField()
    ast = models.FloatField()
    reb = models.FloatField()

    def __str__(self):
        return f"{self.player} ({self.year})"

class AnalysisLog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.date_created.strftime('%Y-%m-%d')}"