from django.db import models
from django.contrib.auth.models import User
import uuid

class PaymentCategory(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title}"

class Student(models.Model):
    LEVEL_CHOICES = [
        ('ND1', 'ND1'),
        ('ND2', 'ND2'),
        ('HND1', 'HND1'),
        ('HND2', 'HND2'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    level = models.CharField(max_length=5, choices=LEVEL_CHOICES)
    school = models.CharField(max_length=100)
    sex = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.full_name}"

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    payment_category = models.ForeignKey(PaymentCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment {self.student} {self.payment_category}"

class Invoice(models.Model):
    payment = models.OneToOneField(
        'Payment',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='invoice'
    )
    pdf = models.FileField(upload_to='invoice/')
    qrcode = models.FileField(upload_to='qrcode/')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice {self.payment.id}"
