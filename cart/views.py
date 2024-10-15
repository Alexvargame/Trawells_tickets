from django.shortcuts import render,redirect, get_object_or_404
from django.views.decorators.http import require_POST
from railway.models import Ticket
from .cart import Cart
from .forms import CartAddTicketForm

@require_POST
def cart_add(request, ticket_id):
    cart=Cart(request)
    ticket=get_object_or_404(Ticket,id=ticket_id)
    form=CartAddTicketForm(request.POST)
    if form.is_valid():
        cd=form.cleaned_data
        cart.add(ticket=ticket,quantity=cd['quantity'],update_quantity=cd['update'])
    return redirect('cart_detail')

def cart_remove(request, ticket_id):
    cart=Cart(request)
    ticket=get_object_or_404(Ticket,id=ticket_id)
    cart.remove(ticket)
    return redirect('cart_detail')

def cart_detail(request):
    cart=Cart(request)
    for item in cart:
        item['update_quantity_form']=CartAddTicketForm(initial={'quantity':item['quantity'], 'update':True})
        
    return render(request,'cart/cart_detail.html',{'cart':cart})
