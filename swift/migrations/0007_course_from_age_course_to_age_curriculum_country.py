# Generated by Django 4.2.1 on 2023-06-06 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swift', '0006_remove_topic_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='from_age',
            field=models.IntegerField(blank=True, null=True, verbose_name='From Age'),
        ),
        migrations.AddField(
            model_name='course',
            name='to_age',
            field=models.IntegerField(blank=True, null=True, verbose_name='To Age'),
        ),
        migrations.AddField(
            model_name='curriculum',
            name='country',
            field=models.CharField(blank=True, choices=[('UK', 'UK'), ('International', 'International')], max_length=100),
        ),
    ]
