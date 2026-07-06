from django.db import models
from users.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    background_image = models.TextField(blank=True, null=True)


class TodoList(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='todo_lists', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "order": self.order,
        }


class Todo(models.Model):
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name='todos', on_delete=models.SET_NULL, null=True, blank=True)
    todo_list = models.ForeignKey(TodoList, related_name='todos', on_delete=models.CASCADE, null=True, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "todo_list": self.todo_list_id,
            "order": self.order,
        }
