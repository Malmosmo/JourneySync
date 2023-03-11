from django.db import models
import uuid

# Create your models here.


#def get_path(instance):
    #return f'data/{instance.pk}/master'


class Room(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    # path = models.FilePathField(path=get_path, allow_files=False, allow_folders=True, unique=True, editable=False)
