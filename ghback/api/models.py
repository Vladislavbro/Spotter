from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribe_until = models.IntegerField(blank=True, null=True)

    def __str__(self):
        user = self.user
        return '{0} {1} {2}'.format(user.first_name, self.patronymic, user.last_name)
