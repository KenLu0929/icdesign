from django.db import models
from django.db import connection
from django.utils import timezone
# Create your models here.


dummy_data = {
    "id": "a",
    "pass": "a",
}

class User(models.Model):
    ic_id = models.CharField(max_length=100, primary_key=True)
    ic_pass = models.CharField(max_length=100)

    class Meta:
        ordering = ['ic_id']
