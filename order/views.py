from django.shortcuts import render,get_object_or_404, redirect
from .models import OrderItem, Order
from .forms import OrderCreateForm, OrderSearchForm, TicketSearchForm
from railway.models import Ticket,ScheduleTrains
from railway.serializers import TicketSerializer
from cart.cart import Cart
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View

from datetime import date, datetime


def order_create(request):
    cart=Cart(request)
    if request.method=='POST':
        form=OrderCreateForm(request.POST)
        if form.is_valid():
            order=form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         ticket=item['ticket'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            return render(request, 'order/created.html',{'order':order})
    else:
        form=OrderCreateForm()
        return render(request, 'order/create.html',{'cart':cart,'form':form})

class OrderSearch(LoginRequiredMixin,View):

    

    def get(self,request):
        

        if request.GET:
            
           
            form=OrderSearchForm(request.GET,initial={'date_b':date(2023,5,1), 'date_e':date(2023,12,31)})
            orders=Order.objects.filter(first_name=request.GET['first_name'],last_name=request.GET['last_name'],
                                        #city=request.GET['city'],address=request.GET['address'],
                                        paid=request.GET['paid'],
                                        updated__range=(request.GET['date_b'],request.GET['date_e']))
            paginator=Paginator(orders,15)
            page=request.GET.get('page')
            try:
                orders=paginator.page(page)
            except PageNotAnInteger:
                orders=paginator.page(1)
            except EmptyPage:
                orders=paginator.page(paginator.num_pages)
            
            
            return render(request, 'order/order_search_list.html',{'orders':orders,'page':page})
        else:
            form=OrderSearchForm(initial={'date_b':date(2023,5,1), 'date_e':date(2023,12,31)})
        return render(request, 'order/order_search.html',{'form':form})


class TicketSearch(LoginRequiredMixin,View):

    

    def get(self,request):
        

        if request.GET:
            
           
            form=TicketSearchForm(request.GET,initial={'date_b':date(2023,5,1), 'date_e':date(2023,12,31)})
            
            trains=ScheduleTrains.objects.filter(date_train__range=(request.GET['date_b'],request.GET['date_e']),train=request.GET['train'])
            tickets=Ticket.objects.filter(date_start__range=(request.GET['date_b'],request.GET['date_e']),
                                          train__in=[tr.train for tr in trains])

##            paginator=Paginator(tickets,15)
##            page=request.GET.get('page')
##            try:
##                tickets=paginator.page(page)
##            except PageNotAnInteger:
##                tickets=paginator.page(1)
##            except EmptyPage:
##                tickets=paginator.page(paginator.num_pages)
            
            
            return render(request, 'order/ticket_search_list.html',{'tickets':tickets})#'page':page,
                                                                    #'s':(trains,tickets,request.GET['date_b'],request.GET['date_e'])})
        else:
            form=TicketSearchForm(initial={'date_b':date(2023,5,1), 'date_e':date(2023,12,31)})
        return render(request, 'order/ticket_search.html',{'form':form})


class OrderItemDetailView(LoginRequiredMixin,View):

    def get(self, request,pk):      
        order=get_object_or_404(OrderItem,id=pk)
        return render(request, 'order/order_item_detail.html',{'order':order})

class OrderDetailView(LoginRequiredMixin,View):

    def get(self, request,pk):      
        order=get_object_or_404(Order,id=pk)
        tickets=[oritem.ticket for oritem in OrderItem.objects.filter(order=order)]
        return render(request, 'order/order_detail.html',{'order':order,'tickets':tickets})


class BookedTickets(LoginRequiredMixin,View):

    

    def get(self,request):
        

        if request.GET:
            
           
            form=OrderSearchForm(request.GET,initial={'date_b':date(2023,5,1), 'date_e':date(2023,12,31)})
            orders=Order.objects.filter(first_name=request.GET['first_name'],last_name=request.GET['last_name'],
                                        #city=request.GET['city'],address=request.GET['address'],
                                        paid=request.GET['paid'],
                                        updated__range=(request.GET['date_b'],request.GET['date_e']))
            orderitems=[item.ticket for item in OrderItem.objects.filter(order__in=orders)]
            booked_tickets=[ticket for ticket in Ticket.objects.filter(booked=True) if ticket in orderitems]
            paginator=Paginator(booked_tickets,15)
            page=request.GET.get('page')
            try:
                booked_tickets=paginator.page(page)
            except PageNotAnInteger:
                booked_tickets=paginator.page(1)
            except EmptyPage:
                booked_tickets=paginator.page(paginator.num_pages)
            
            
            return render(request, 'order/booked_tickets_list.html',{'booked_tickets':booked_tickets,'page':page})
        else:
            form=OrderSearchForm(initial={'date_b':date(2023,5,1), 'date_e':date(2023,12,31)})
        return render(request, 'order/booked_tickets.html',{'form':form})


class CheckBooked(LoginRequiredMixin,View):

    def get(self, request,pk):
      
        ticket=get_object_or_404(Ticket,id=pk)
        serializer=TicketSerializer(ticket)
        return render(request,'order/check_booked.html',{'ticket':ticket})
  

class ConfirmBooked(LoginRequiredMixin,View):

    def get(self, request,pk):
      
        ticket=get_object_or_404(Ticket,id=pk)
        serializer=TicketSerializer(ticket)
        return render(request,'order/confirm_booked.html',{'ticket':ticket})

    def post(self, request,pk):
      
        ticket=get_object_or_404(Ticket,id=pk)
        serializer=TicketSerializer(ticket)
        ticket.booked=False
        ticket.save()
        return redirect(ticket)
  
class CancelBooked (LoginRequiredMixin,View):
    def post(self, request,pk):
      
        ticket=get_object_or_404(Ticket,id=pk)
        serializer=TicketSerializer(ticket)
        #ticket.booked=False
        
        ticket.train.tickets+=':'+str((ticket.carriage,ticket.place))
        ticket.detete()
        return redirect(ticket)










    
