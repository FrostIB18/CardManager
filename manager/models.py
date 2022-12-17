from django.db import models
from model_utils.fields import StatusField
from model_utils import Choices

# Create your models here.
class Card(models.Model):
    STATUS = Choices('Активирована', 'Не активирована', 'Просрочена')
    series = models.CharField(max_length=10)
    number = models.CharField(max_length=20, unique=True)
    release_date = models.DateTimeField()
    expiration_date = models.DateTimeField()
    usage_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    status = StatusField()

    def __str__(self):
        return f'Номер карты: {self.number} - Cумма: {self.amount}'