from decimal import Decimal
from django.conf import settings
from railway.models import Ticket

class Cart(object):

    def __init__(self, request):
        self.session=request.session
        cart=self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart=self.session[settings.CART_SESSION_ID]={}
        self.cart=cart

    def add(self, ticket,quantity=1, update_quantity=False):
        ticket_id=str(ticket.id)
        if ticket_id not in self.cart:
            self.cart[ticket_id]={'quantity':0,'price':str(ticket.price)}
        if update_quantity:
            self.cart[ticket_id]['quantity']=quantity
        else:
            self.cart[ticket_id]['quantity']+=quantity
        self.save()

    def save(self):
        self.session.modified=True

    def remove(self, ticket):
        ticket_id=str(ticket.id)
        if ticket_id in self.cart:
            del self.cart[ticket_id]
            self.save()

    def __iter__(self):
        ticket_ids=self.cart.keys()
        tickets=Ticket.objects.filter(id__in=ticket_ids)

        cart=self.cart.copy()
        for ticket in tickets:
            cart[str(ticket.id)]['ticket']=ticket
        for item in cart.values():
            item['price']=Decimal(item['price'])
            item['total_price']=item['price']*item['quantity']
            yield item
        
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price'])*item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
        
    
        
