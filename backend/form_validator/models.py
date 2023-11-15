from django.db import models


class FormTemplate(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.BooleanField(default=False)
    phone = models.BooleanField(default=False)
    date = models.BooleanField(default=False)
    text = models.BooleanField(default=False)
