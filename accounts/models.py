from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from social_network.constant import STATUS

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at', 'username']

    def __str__(self):
        return str(self.username)

class Friendship(models.Model):
    from_user = models.ForeignKey(User, related_name='friendship_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friendship_requests_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Friendship'
        verbose_name_plural = 'Friendships'
        ordering = ['-created_at']


