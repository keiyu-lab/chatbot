# Generated by Django 4.2.7 on 2023-12-08 06:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chatbot_app", "0004_alter_qacache_created_time_alter_qacache_question"),
    ]

    operations = [
        migrations.AlterField(
            model_name="qacache",
            name="answer",
            field=models.TextField(unique=True),
        ),
    ]
