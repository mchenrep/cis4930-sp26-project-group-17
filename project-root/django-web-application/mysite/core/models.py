from django.db import models

# Define models
class Repository(models.Model):
    full_name = models.CharField(max_length=1000)
    stars = models.IntegerField(default=0)
    language = models.CharField(max_length=100)
    url = models.CharField(max_length=1000)
    created_at = models.CharField(max_length=1000) # kept as charfield to make integrating data easier

    def __str__(self):
        return f"Repository Name: {self.full_name}\nStars: {self.stars}\nLanguage: {self.language}\nURL: {self.url}\nCreated: {self.created_at}"
