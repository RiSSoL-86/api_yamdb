from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Title(models.Model):
    """Затычка для модели title."""
