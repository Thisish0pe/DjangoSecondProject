# Generated by Django 4.2.3 on 2023-07-28 08:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chatbot', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='questioner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversation', to=settings.AUTH_USER_MODEL),
        ),
    ]