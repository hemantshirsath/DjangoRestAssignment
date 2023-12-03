from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class WorkType(models.TextChoices):
    YOUTUBE = 'YT', 'Youtube'
    INSTAGRAM = 'IG', 'Instagram'
    OTHER = 'OT', 'Other'

class Work(models.Model):
    link = models.URLField(max_length=255)
    work_type = models.CharField(max_length=2, choices=WorkType.choices)

    def __str__(self):
        return self.link

class Artist(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    works = models.ManyToManyField(Work, related_name='artists')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('artist-detail', kwargs={'pk': self.pk})
