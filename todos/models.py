from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Todo(models.Model):
    description = models.TextField()
    status = models.BooleanField(default=False)  # False for pending, True for complete
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, related_name='todos', on_delete=models.CASCADE)

    def __str__(self):
        return self.description
