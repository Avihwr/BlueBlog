# Generated by Django 3.1 on 2020-08-29 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blog_excerpt_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='tag',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
