from django.db import models

class Coffee(models.Model):
    name = models.CharField(max_length=100)
    amount = models.CharField(max_length=10000)
    payment_id = models.CharField(max_length=10000)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.name