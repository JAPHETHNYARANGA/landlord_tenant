from django.db import models
from users.models import Tenant
from properties.models import Property




class MaintenanceTicket(models.Model):
   ISSUE_TYPE_CHOICES =[
       ('Plumbing', 'Plumbing'),
       ('Electrical','Electrical'),
       ('Heating','Heating'),
       ('Other', 'Other'),
   ]


   STATUS_CHOICES = [
       ('Open','Open'),
       ('In Progress','In Progress'),
       ('Resolved', 'Resolved'),
       ('Closed', 'Closed'),
   ]


   ticket_id = models.AutoField(primary_key=True)
   tenant_id = models.ForeignKey(Tenant,on_delete=models.CASCADE )
   property_id  = models.ForeignKey(Property, on_delete=models.CASCADE)
   issue_type = models.CharField(max_length=50, choices=ISSUE_TYPE_CHOICES)
   description = models.TextField()
   status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='Open')
   released_date = models.DateField()
   resolved_date = models.DateField(null=True, blank=True)


   def __str__(self):
       return  f"Ticket {self.ticket_id}:{self.issue_type}-{self.status}"
  





