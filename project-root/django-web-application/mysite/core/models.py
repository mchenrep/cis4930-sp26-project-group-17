from django.db import models

# Define models
class Repository(models.Model):
    repo_name = models.CharField(max_length=1000)
    username = models.CharField(max_length=200)
    stars = models.IntegerField(default=0)
    language = models.CharField(max_length=100)
    url = models.CharField(max_length=1000)
    created_at = models.CharField(max_length=1000) # kept as charfield to make integrating data easier

    def __str__(self):
        return f"{self.repo_name} ({self.stars})"

class NbaStat(models.Model):
    player = models.CharField(max_length=200)
    team = models.CharField(max_length=10)
    gp = models.IntegerField(null=True, blank=True)
    pts = models.FloatField(null=True, blank=True)
    ast = models.FloatField(null=True, blank=True)
    reb = models.FloatField(null=True, blank=True)
    eff = models.FloatField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.player} ({self.year})"

class AnalysisLog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_created = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.date_created.strftime('%Y-%m-%d')}"