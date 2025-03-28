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

    def __str__(self):
        return (f'{self.email}, {self.role}')



class Feedbacks(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    TITLE = (
        ('complain', 'complain'),
        ('compliment', 'compliment'),
    )
    title = models.CharField(max_length=100, choices=TITLE, default="complain")
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
    message = models.TextField()
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
    
    def __str__(self):
        return (f'{self.user_id}, {self.category}, {self.status}')


class AdminResponse(models.Model):
    response_id = models.AutoField(primary_key=True)
    admin_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    feedback_id = models.ForeignKey(Feedbacks, on_delete=models.CASCADE)
    message = models.TextField()
    response_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f'{self.admin_id}, {self.user_id}, {self.response_date}')

class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    month = models.CharField(max_length=100)
    total_complaints = models.IntegerField()
    total_compliments = models.IntegerField()
    total_feedbacks = models.IntegerField()
    report_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f'{self.month}, {self.report_date}')



