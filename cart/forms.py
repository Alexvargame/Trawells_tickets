from django import forms

TICKET_QUANTITY_CHOICE=[(i,str(i)) for i in range(1,36)]

class CartAddTicketForm(forms.Form):

    quantity=forms.TypedChoiceField(choices=TICKET_QUANTITY_CHOICE, coerce=int)
    update=forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)

    
    
