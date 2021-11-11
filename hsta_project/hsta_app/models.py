from django.db import models
import os
from django.conf import settings


# Create your models here.

class HstaData(models.Model):
    ISBN = models.CharField(max_length=10000000, blank=True)
    title = models.CharField(max_length=10000000, blank=True)
    author = models.CharField(max_length=10000000, blank=True)
    chapter = models.CharField(max_length=10000000, blank=True)
    zip_file = models.FileField(blank=True, null=True)
    edition = models.CharField(max_length=10000000, blank=True)
    email = models.CharField(max_length=10000000, blank=True)

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.zip_file.name))
        super(HstaData, self).delete(*args, **kwargs)


class UploadedInputsInfo(models.Model):
    user_names = models.CharField(max_length=10000000)
    file_names = models.CharField(max_length=10000000)
    output_status = models.CharField(max_length=10000000)
    date = models.CharField(max_length=10000000, blank=True)
