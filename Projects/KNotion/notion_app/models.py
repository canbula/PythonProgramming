from django.db import models

class Book(models.Model):
    STATUS_CHOICES = [
        ('not-started', 'Not started'),
        ('reading', 'Reading'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    image = models.URLField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not-started')

    def __str__(self):
        return self.title
