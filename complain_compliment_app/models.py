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

class Feedbacks(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    message = models.TextField()
    CATEGORY = (
        ('academic', 'academic'),
        ('finance', 'finance'),
        ('hostel', 'hostel'),
        ('library', 'library'),
        ('medical', 'medical'),
        ('security', 'security'),
        ('transport', 'transport'),
        ('complaint', 'complaint'),
    )
    category = models.CharField(max_length=100, choices=CATEGORY)
    STATUS = (
        ('pending', 'pending'),
        ('on-progress', 'on-progress'),
        ('resolved', 'resolved'),
    )
    status = models.CharField(max_length=100, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk:
            original = Feedbacks.objects.get(pk=self.pk)
            if original.status != self.status:
                from django.utils.timezone import now
                self.updated_at = now()
        super().save(*args, **kwargs)


