# Generated by Django 5.1.7 on 2025-03-30 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complain_compliment_app', '0004_report_feedbacks_title_alter_feedbacks_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminresponse',
            name='response',
            field=models.TextField(default=''),
        ),
    ]
