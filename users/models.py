from django.contrib.auth.models import AbstractUser
from djongo import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    display_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.display_name or self.username


class Follow(models.Model):
    follower = models.ForeignKey(
        'CustomUser',
        related_name='following_set',
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        'CustomUser',
        related_name='followers_set',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower} -> {self.following}'
