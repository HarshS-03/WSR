import json
from customer.models import Product
from django.contrib import messages
from django.core.mail import send_mail

def registrationMail(email):
    msg=f'Thank you for Registering with us. \n Exlplore our new products at lowest rate and best service in the Town.\n\nbest regards,\nWSR Team'
    send_mail("Welcome to WSR-Family",
                  msg,
                   "shrimaliharsh152@gmail.com",
                  [email],
                  fail_silently=True)
    
    
def confirmationMail(email,orderid):
    link=f'http://127.0.0.1:8000/customer/ordertrack/{orderid}'
    msg=f'Your order has been confirmed for order id {orderid}' + f'\nClick on this link to track your order {link}'
    send_mail("WSR order confirmed",
                  msg,
                   "shrimaliharsh152@gmail.com",
                  [email],
                  fail_silently=True)    


def updateCart(request,productDetails):
    products=json.loads(productDetails)
    for item in products:
        name = products[item][0]
        allProducts = Product.objects.get(name=name)
        qty = allProducts.qty
        qty = qty -products[item][2]
        if qty < 0 :
            msg=f'Sorrry but we can\'t able to satisfy your request for {name}. We have only {allProducts.qty} items in our stock.'
            messages.warning(request,msg)
            return False
        else :
            allProducts.qty = qty        
            allProducts.save()
            return True
        
    
def prodDetail(prodDetail):
    products=json.loads(prodDetail)
    data=''
    for item in products:
        str=f'{products[item][0]} ({products[item][1]} * {products[item][2]})\n'
        data+=str
    return data
    