from django.db import models
from django.urls import reverse

class Item(models.Model):
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=80, blank=True)
    description = models.TextField(blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("item_detail", kwargs={"pk": self.pk})
