from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.postgres.fields import JSONField
import json
from django.contrib.admin.models import LogEntry




class Vendor(models.Model):
    name = models.CharField(max_length=100) 
    contact_details = models.TextField(max_length=10, blank=True)  
    address = models.TextField(max_length=200, blank=True)  
    vendor_code = models.CharField(max_length=50, unique=True)  
    on_time_delivery_rate = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5)]) 
    quality_rating_avg = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5)]) 
    average_response_time = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5)]) 
    fulfillment_rate = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5)]) 

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('complete', 'Complete'),
        ('canceled', 'Canceled'),
    ]

    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField() 
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending') 
    quality_rating = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    issue_date = models.DateTimeField(null=True, blank=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)


    @receiver(pre_save, sender='api.PurchaseOrder')
    def update_quantity(sender, instance, **kwargs):
        if isinstance(instance.items, str):
            instance.items = json.loads(instance.items)
        if isinstance(instance.items, list):
            instance.quantity = len(instance.items)
            pass
        else:
            print("Instance does not have 'items'")
        
    def save(self, *args, **kwargs):
        if not self.delivery_date:
            self.delivery_date = self.order_date + timedelta(days=2)

        if self.status == 'complete' and not self.issue_date:
            self.issue_date = timezone.now()

        if self.status == 'canceled' and not self.acknowledgment_date:
            self.acknowledgment_date = timezone.now()

        if self.status == 'complete':
            self.acknowledgment_date = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.po_number} - {self.vendor.name} -{self.id}"
    

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    on_time_delivery_rate = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    quality_rating_avg = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    average_response_time = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"