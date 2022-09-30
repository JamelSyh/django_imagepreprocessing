# Generated by Django 4.1 on 2022-09-29 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_processing_alter_image_category"),
    ]

    operations = [
        migrations.RenameField(
            model_name="processing", old_name="type", new_name="type1",
        ),
        migrations.RemoveField(model_name="image", name="category",),
        migrations.AddField(
            model_name="processing",
            name="type2",
            field=models.CharField(default="none", max_length=32),
        ),
        migrations.AddField(
            model_name="processing",
            name="type3",
            field=models.CharField(default="none", max_length=32),
        ),
    ]