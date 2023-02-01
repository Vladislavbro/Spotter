from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, blank=True, null=True)
    subscribe_type = models.CharField(max_length=100, blank=True, null=True)
    subscribe_until = models.IntegerField(blank=True, null=True)

    def __str__(self):
        user = self.user
        return '{0} {1}'.format(user.first_name, user.last_name)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateTimeField()
    subscribe_type = models.CharField(max_length=100, blank=True, null=True)
    amount = models.IntegerField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        user = self.user
        return '{0} {1} {2}'.format(user.first_name, user.last_name, self.date)
