import uuid

from django.db import models

class Genre:
    app_label = 'genre_app'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    categories = models.ManyToManyField('category_app.Category', related_name='genres')

    class Meta:
        db_table = 'Genre'