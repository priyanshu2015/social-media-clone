# Generated by Django 4.2.7 on 2023-11-18 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_post_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='detail',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]