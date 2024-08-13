from django.db import models
from users.models  import Tenant
from  properties.models import Property

class  RentPayment(models.Model):
    PAYMENT_METHOD_CHOICES  = [
        ('cash','cash'),
        ('credit_card','Credit Card'),
        ('bank_transfer','Bank Transfer'),
        ('mobile_money','Mobile Money'),
    ]

    payment_id =  models.AutoField(primary_key=True)
    tenant_id = models.ForeignKey('Tenant', on_delete=models.CASCADE)
    property_id  =  models.ForeignKey('Property', on_delete=models.CASCADE)
    amount  = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date  = models.DateTimeField(auto_now_add=True)
    payment_method  = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)


 

    def __str__(self):
        return f'Payment {self.payment_id} - {self.amount}'
