# Generated by Django 4.2.3 on 2023-07-31 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0003_alter_conversation_questioner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='prompt',
            field=models.CharField(max_length=312),
        ),
    ]
