from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from PIL import Image
import re
import os

# Opcions de categories dels esdeveniments
CATEGORY_CHOICES = [
    ('gaming', 'Gaming'),
    ('music', 'Música'),
    ('talk', 'Xerrades'),
    ('education', 'Educació'),
    ('sports', 'Esports'),
    ('entertainment', 'Entreteniment'),
    ('technology', 'Tecnologia'),
    ('art', 'Art i Creativitat'),
    ('other', 'Altres'),
]

# Opcions d'estat dels esdeveniments
STATUS_CHOICES = [
    ('scheduled', 'Programat'),
    ('live', 'En Directe'),
    ('finished', 'Finalitzat'),
    ('cancelled', 'Cancel·lat'),
]

class Event(models.Model):
    # Camps bàsics
    title = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events_created')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    scheduled_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    thumbnail = models.ImageField(upload_to='events/thumbnails/', blank=True, null=True)
    max_viewers = models.PositiveIntegerField(default=100)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=500, blank=True, null=True)
    stream_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

    # Retorna la URL detallada de l'esdeveniment
    def get_absolute_url(self):
        return reverse('events:event_detail', args=[self.pk])

    # Propietats per verificar l'estat
    @property
    def is_live(self):
        return self.status == 'live'

    @property
    def is_upcoming(self):
        return self.status == 'scheduled' and self.scheduled_date > timezone.now()

    # Durada estimada segons la categoria
    def get_duration(self):
        category_durations = {
            'gaming': 180,
            'music': 90,
            'talk': 60,
            'education': 120,
            'sports': 150,
            'entertainment': 120,
            'technology': 90,
            'art': 120,
            'other': 90,
        }
        return timedelta(minutes=category_durations.get(self.category, 90))

    # Llista de tags separats per comes
    @property
    def get_tags_list(self):
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    # URL embebida per al vídeo
    @property
    def get_stream_embed_url(self):
        if not self.stream_url:
            return None

        url = self.stream_url

        # YouTube curt
        if "youtu.be" in url:
            video_id = url.split("/")[-1]
            return f"https://www.youtube.com/embed/{video_id}"

        # YouTube normal
        if "watch?v=" in url:
            video_id = url.split("watch?v=")[-1].split("&")[0]
            return f"https://www.youtube.com/embed/{video_id}"

        # Altres URLs (Twitch, Vimeo, etc.)
        return url

    # Miniatura del vídeo segons la URL
    @property
    def get_stream_thumbnail(self):
        if not self.stream_url:
            return None
        url = self.stream_url.strip()

        # YouTube
        youtube = re.match(r'.*(?:youtube\.com/watch\?v=|youtu\.be/)([A-Za-z0-9_\-]+)', url)
        if youtube:
            return f'https://img.youtube.com/vi/{youtube.group(1)}/hqdefault.jpg'

        # Twitch (placeholder)
        twitch = re.match(r'.*twitch\.tv/([^/]+)', url)
        if twitch:
            return '/static/events/twitch_placeholder.jpg'

        # Vimeo (placeholder)
        vimeo = re.match(r'.*vimeo\.com/([0-9]+)', url)
        if vimeo:
            return '/static/events/vimeo_placeholder.jpg'

        return None

    # Sobreescriu el save per redimensionar imatges
    def save(self, *args, **kwargs):
        try:
            old_instance = Event.objects.get(pk=self.pk)
        except Event.DoesNotExist:
            old_instance = None

        super().save(*args, **kwargs)

        # Redimensiona la miniatura
        if self.thumbnail:
            img_path = self.thumbnail.path
            img = Image.open(img_path)
            max_size = (800, 450)
            img.thumbnail(max_size)
            img.save(img_path)
        elif old_instance and old_instance.thumbnail and not self.thumbnail:
            old_path = old_instance.thumbnail.path
            if os.path.exists(old_path):
                os.remove(old_path)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Esdeveniment'
        verbose_name_plural = 'Esdeveniments'
        