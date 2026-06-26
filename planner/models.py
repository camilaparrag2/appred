"""
Modelos de la aplicacion FeedPlan: MediaPost y AgendaItem.
"""
from django.db import models
from django.contrib.auth.models import User


class MediaPost(models.Model):
    """
    Almacena las imagenes que el usuario sube para previsualizar en sus feeds.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='feeds/')
    order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-uploaded_at']

    def __str__(self):
        filename = self.image.name.split('/')[-1] if self.image else 'sin archivo'
        return f"Imagen #{self.order} - {filename}"


class AgendaItem(models.Model):
    """
    Representa un post planificado dentro de la agenda semanal del emprendedor.
    """
    POST_TYPES = [
        ('IMG', 'Imagen'),
        ('CAR', 'Carrusel'),
        ('REL', 'Reel'),
    ]

    DAYS = [
        ('LU', 'Lunes'),
        ('MA', 'Martes'),
        ('MI', 'Miercoles'),
        ('JU', 'Jueves'),
        ('VI', 'Viernes'),
        ('SA', 'Sabado'),
        ('DO', 'Domingo'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    post_type = models.CharField(max_length=3, choices=POST_TYPES, default='IMG')
    day = models.CharField(max_length=2, choices=DAYS)
    time = models.TimeField(blank=True, null=True)
    notes = models.TextField(blank=True)
    images = models.ManyToManyField(MediaPost, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['day', 'time', '-created_at']

    def __str__(self):
        return f"{self.get_day_display()} - {self.title} ({self.get_post_type_display()})"
