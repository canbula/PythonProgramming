from django.db import models
from user.models import CustomUser

class Workspace(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='workspaces')
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True, null=True, default='fa-solid fa-w')  # Default FontAwesome icon
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(CustomUser, related_name='shared_workspaces', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.members.filter(id=self.user.id).exists():
            self.members.add(self.user)

    def __str__(self):
        return self.name

class Page(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='pages')
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True, null=True, default='fa-solid fa-file')
    content = models.TextField(blank=True)  # Add content field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title