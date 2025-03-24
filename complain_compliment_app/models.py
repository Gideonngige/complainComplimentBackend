from django.db import models

# Create your models here.
class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100)
    ROLES = (
        ('admin', 'admin'),
        ('lecturer', 'lecturer'),
        ('staff', 'staff'),
        ('student', 'student'),
    )
    role = models.CharField(max_length=100, choices=ROLES)
    password = models.CharField(max_length=100)
