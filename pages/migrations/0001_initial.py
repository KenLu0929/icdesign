# Generated by Django 3.2.5 on 2021-07-16 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ic_id', models.CharField(max_length=100)),
                ('ic_pass', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['ic_id'],
            },
        ),
    ]
