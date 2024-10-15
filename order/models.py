from django.db import models
from railway.models import Ticket
from django.shortcuts import reverse
class Order(models.Model):

    first_name=models.CharField(max_length=50, null=True, blank=True)
    last_name=models.CharField(max_length=50, null=True, blank=True)
    email=models.EmailField(blank=True)
    address=models.CharField(max_length=250, null=True, blank=True)
    postal_code=models.CharField(max_length=20, null=True, blank=True)
    city=models.CharField(max_length=100, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    paid=models.BooleanField(default=False)

    class Meta:
        ordering=('-created',)
        verbose_name='Покупатель'
        verbose_name_plural='Покупатели'

    def __str__(self):
        return 'Order {}'.format(self.id)
    def get_absolute_url(self):
        return reverse('order_detail_url',kwargs={'pk':self.id})

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order=models.ForeignKey(Order, related_name='items', on_delete=models.DO_NOTHING)
    ticket=models.ForeignKey(Ticket, related_name='order_items', on_delete=models.DO_NOTHING)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price*self.quantity

    def get_absolute_url(self):
        return reverse('order_item_detail_url',kwargs={'pk':self.id})
    
    
