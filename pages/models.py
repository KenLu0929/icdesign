from django.db import models

# Create your models here.

from django.db import connection


def get_users():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM testing")
        row = cursor.fetchall()

    return row
