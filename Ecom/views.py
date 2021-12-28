from django import http
from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Order, Product,Categories,Variant,OrderItem,ShippingAddress,OrderUpdates
from math import ceil
import datetime
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from . import record_type
from templates import voice
from templates import sr_script
from templates import speakBot
from templates import tapTheProduct

# Create your views here.
def Elogin(request):
    if request.method=="POST":
        loginusername=request.POST["loginusername"]
        loginPassword=request.POST["loginpassword"]
        user=authenticate(username=loginusername,password=loginPassword)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Logged In")
        else:
            messages.error(request,"Invalid Username Or Password !")

        return redirect("/")
def Elogout(request):
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return redirect("/")
def Esignup(request):
    if request.method=="POST":
        username=request.POST["username"]
        fname=request.POST["fname"]
        lname=request.POST["lname"]
        email=request.POST["email"]
        pass1=request.POST["pass1"]
        pass2=request.POST["pass2"]
    
        if(pass1!=pass2):
            messages.error(request,"Your Passwords Are Not Same!")
            return redirect("/")
        # print(checkUser)
        try:
            checkUser=User.objects.get(username=username)
            
        except Exception as e:
            myuser=User.objects.create_user(username,email,pass1)
            myuser.first_name=fname
            myuser.last_name=lname
            myuser.save()
            user=authenticate(username=username,password=pass1)
            login(request,user)
            messages.success(request,"Successfully Signed In")
            return redirect("/")
            
        messages.error(request,"This Username Has Already Been Taken")   
        return redirect("/")
def checkUser(request):
    if request.method=="POST":
        username=request.POST["username"]

        try:
            user=User.objects.get(username=username)
            return HttpResponse("no")
        except Exception as e:
            return HttpResponse("yes")

        
        
def Ehome(request):
    record_type.type=0
    cats=Categories.objects.all()
    n=len(cats)
    # slides=n//4+ceil((n/4)-(n//4))
    products=Product.objects.all().order_by('product_id')

    if request.user.is_authenticated:
        customer=request.user
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        cartItems=order.get_cart_items
    else:
        cartItems=0

    allProds=Paginator(products,6)
    page=request.GET.get('page')
    try:
        prods=allProds.page(page)
    except PageNotAnInteger:
        prods=allProds.page(1)
    except EmptyPage:
        prods=allProds.page(allProds.num_pages)

    param={"categories":cats,"slides":n,"range":range(1,n),"products":prods,"cartItems":cartItems}
    print(param['range'])
    return render(request,"Ecom/Ehome.html",param)

def Eabout(request):
    if request.user.is_authenticated:
        customer=request.user
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        cartItems=order.get_cart_items
    else:
        cartItems=0
    cats=Categories.objects.all()
    return render(request,"Ecom/Eabout.html",{"categories":cats,"cartItems":cartItems})
def Econtact(request):
    if request.user.is_authenticated:
        customer=request.user
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        cartItems=order.get_cart_items
    else:
        cartItems=0
    cats=Categories.objects.all()
    return render(request,"Ecom/Econtact.html",{"categories":cats,"cartItems":cartItems})



def showCategory(request,category):
    cats=Categories.objects.all()
    cat=Categories.objects.filter(category=category).first()
    products=Product.objects.filter(category=cat)

    if request.user.is_authenticated:
        customer=request.user
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        cartItems=order.get_cart_items
    else:
        cartItems=0
    return render(request,"Ecom/categoryProducts.html",{"products":products,"category":category,"categories":cats,"cartItems":cartItems})


def showProduct(request,prod_id):
    product=Product.objects.filter(product_id=prod_id).first()
    variants=Product.objects.filter(product_id=prod_id).values("variant")
    variants=[variants["variant"] for variants in variants]
    allVariants=[]
    for variant in variants:
        prod_variant=Variant.objects.filter(id=variant)[0]
        allVariants.append(prod_variant)
    cats=Categories.objects.all()
    #tapTheProduct.run_voice()
    if request.user.is_authenticated:
        customer=request.user
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        cartItems=order.get_cart_items
    else:
        cartItems=0
    # print(record_type.type)
    if(record_type.type==1):
        return render(request,"Ecom/showProd_mic.html",{"product":product,"variants":allVariants,"categories":cats,"cartItems":cartItems})

    return render(request,"Ecom/showProduct.html",{"product":product,"variants":allVariants,"categories":cats,"cartItems":cartItems})

def cart(request):
    if request.user.is_authenticated:
        customer=request.user
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order={"get_cart_total":0,"get_cart_items":0}
        get_cart_items=0
        cartItems=0
    
    cats=Categories.objects.all()
    return render(request,"Ecom/cart.html",{"items":items,"order":order,"cartItems":cartItems,"categories":cats})


def update_item(request):
    if request.method=="POST":
        productId=request.POST["productId"]
        action=request.POST["action"]
        variant=request.POST["variant"]
        variant=Variant.objects.get(variant=variant)
        product=Product.objects.get(product_id=productId)
        print(productId,action,variant)
        if(record_type.type==1):
            if request.user.is_authenticated:
                customer=request.user
                order,created=Order.objects.get_or_create(customer=customer,complete=False)
            else:
                order=Order.objects.create(complete=False)
            orderItem,created=OrderItem.objects.get_or_create(order=order,product=product,variant=variant)
            orderItem.quantity=(orderItem.quantity+1)
            that_order=order.id
            that_orderItem=orderItem.id
            orderItem.save()
            order.save()
            return JsonResponse({"order":that_order,"orderItem":that_orderItem})

        customer=request.user
        # print(customer,product)

        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        orderItem,created=OrderItem.objects.get_or_create(order=order,product=product,variant=variant)

        if action=="add":
            orderItem.quantity=(orderItem.quantity+1)
        elif action=="remove":
            orderItem.quantity=(orderItem.quantity-1)
        orderItem.save()
        order.save()
        if orderItem.quantity<=0:
            orderItem.delete()
        return HttpResponse("completed")

def Echeckout(request):
    print("came in wrong__________________________________")
    if request.user.is_authenticated:
        customer=request.user
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        cartItems=order.get_cart_items
        cats=Categories.objects.all()

    if request.method=="POST":
        fname=request.POST["ftname"]
        lname=request.POST["ltname"]
        address=request.POST["address"]
        city=request.POST["city"]
        state=request.POST["state"]
        pincode=request.POST["pincode"]
        phone=request.POST["phone"]
        transactionid=datetime.datetime.now().timestamp()
        
        if request.user.is_authenticated:
            print(fname,lname,address,city,state,pincode,phone,transactionid)
            # total=order.get_cart_total
            order,created=Order.objects.get_or_create(customer=request.user,complete=False)
            # print(order)
            order.complete=True
            # order.transaction_id=transactionid

            orderedItem=OrderItem.objects.filter(order=order).first()
            # print(orderedItem)
            orderUpdate=OrderUpdates(ordered_item=orderedItem,description="Your Ordered Has Been Placed!")
            orderUpdate.save()

            orderedItem.delivery_status="PLACED"
            orderedItem.save()


            order.save()
            orderDetail=ShippingAddress(customer=customer,first_name=fname,last_name=lname,order=order,address=address,city=city,state=state,pincode=pincode,phone=phone)
            orderDetail.save()           

            

            # OrderUpdate=OrderUpdates(ordered_item=orderedItem,description="Your Ordered Has Been Placed !")
            # OrderUpdate.save()
            # messages.success(request,"Order Has Placed Successfully")
            return redirect("/paymentMode/")
        messages.success(request,"Please Login/Signup For shopping!")
        return redirect("/")


    
    return render(request,"Ecom/Echeckout.html",{"categories":cats,"cartItems":cartItems})

def checkout_mic(request,order_id):
    print("got ",order_id)
    if request.method=="POST":
        fname=request.POST["ftname"]
        lname=request.POST["ltname"]
        address=request.POST["address"]
        city=request.POST["city"]
        state=request.POST["state"]
        pincode=request.POST["pincode"]
        phone=request.POST["phone"]
        transactionid=datetime.datetime.now().timestamp()
        
        if request.user.is_authenticated:
            print("authenticated_______________________",request.user)
            customer=request.user
            print(fname,lname,address,city,state,pincode,phone,transactionid)
            # total=order.get_cart_total
            order,created=Order.objects.get_or_create(customer=request.user,complete=False)
            print(")))))))))) order")
            print(order)
            order.complete=True
            # order.transaction_id=transactionid

            orderedItem=OrderItem.objects.filter(order=order).first()
            print(")))))))))))___________________")
            print(orderedItem)
            orderUpdate=OrderUpdates(ordered_item=orderedItem,description="Your Ordered Has Been Placed!")
            orderUpdate.save()

            orderedItem.delivery_status="PLACED"
            orderedItem.save()


            order.save()
            orderDetail=ShippingAddress(customer=customer,first_name=fname,last_name=lname,order=order,address=address,city=city,state=state,pincode=pincode,phone=phone)
            orderDetail.save()           

            

            # OrderUpdate=OrderUpdates(ordered_item=orderedItem,description="Your Ordered Has Been Placed !")
            # OrderUpdate.save()
            messages.success(request,"Order Has Placed Successfully")
            return redirect("/")
        else:
            print("not authenticated____________________")
            order,created=Order.objects.get_or_create(id=order_id,complete=False)

            new_user="defaultuser"+str(order_id)
            new_user_password="default"+str(order_id)
            # default_email=f"default{str(order_id)}@gmail.com"
            default_user=User.objects.create_user(new_user)
            default_user.set_password=new_user_password
            default_user.save()

            default_user=User.objects.get(username=new_user)
            order.customer=default_user
            print(order)
            order.complete=True
            # order.transaction_id=transactionid

            orderedItem=OrderItem.objects.filter(order=order).first()
            print(orderedItem)
            orderUpdate=OrderUpdates(ordered_item=orderedItem,description="Your Ordered Has Been Placed!")
            orderUpdate.save()

            orderedItem.delivery_status="PLACED"
            orderedItem.save()


            order.save()
            orderDetail=ShippingAddress(first_name=fname,last_name=lname,order=order,address=address,city=city,state=state,pincode=pincode,phone=phone)
            orderDetail.save()
            messages.success(request,"Order Has Placed Successfully")
            return redirect("/")
        # messages.success(request,"Please Login/Signup For shopping!")
        return redirect("/")


    
    return render(request,"Ecom/checkout_mic.html",{"order_id":order_id})


def paymentMode(request):
    cats=Categories.objects.all()

    if request.user.is_authenticated:
        customer=request.user
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        cartItems=order.get_cart_items
    else:
        cartItems=0
    return render(request,"Ecom/paymentMode.html",{"categories":cats,"cartItems":cartItems})


def checksearch(query,productName):
    lis=[]
    query=query.lower()
    query_lis=''.join(query).split()    
    productName=str(productName)
    productName=productName.lower()
    lis=''.join(productName).split()
      
    if set(query_lis).issubset(set(lis)):
        return True
    return False               


def searchQuery(request):

    if request.method=="GET":
        
        query=""   
        if 'UseMic' in request.GET:
            # print(record_type.type)
            record_type.type=1
            # print(record_type.type)
            query=sr_script.run_voice()
        else:
            record_type.type=0
            # searchedQuery=query   
            query=request.GET.get("searchQuery").lower()
            
        products=Product.objects.all().values("product_name")
        
        prodList=[product["product_name"] for product in products if checksearch(query,product["product_name"])]
            

        Prods=[]
        for product in prodList:
            prod=Product.objects.filter(product_name=product).first()
            Prods.append(prod)
        cat=Categories.objects.filter(category__icontains=query).first()
        
        if cat != None:
            cat_id=cat.id   
            product_category=Product.objects.filter(category=cat_id)
        else:
            cat_id=None  
            product_category=Product.objects.none()  
        lis1=product_category

        varid=Variant.objects.filter(variant__icontains=query).first()
        if varid != None:
            variant_id=varid.id
            product_variant=Product.objects.filter(variant=variant_id)
        else:
            variant_id=None
            product_variant=Product.objects.none() 
        lis2=product_variant   
        allProds=list(set().union(Prods,lis1,lis2))
                    
        # print(allProds)
        cats=Categories.objects.all()
        
        if request.user.is_authenticated:
            customer=request.user
            order,created=Order.objects.get_or_create(customer=customer,complete=False)
            cartItems=order.get_cart_items
        else:
            cartItems=0
    speak_products=[]
    speak_products=allProds
    # print(record_type.type)
    if(record_type.type==1):
        allProds=Paginator(allProds,4)
        page=request.GET.get('page')
        try:
            prods=allProds.page(page)
        except PageNotAnInteger:
            prods=allProds.page(1)
        except EmptyPage:
            prods=allProds.page(allProds.num_pages)
        return render(request,"Ecom/mic_search.html",{"searchProducts":prods,"searchedQuery":query,"speak_products":speak_products})
    
    allProds=Paginator(allProds,6)
    page=request.GET.get('page')
    try:
        prods=allProds.page(page)
    except PageNotAnInteger:
        prods=allProds.page(1)
    except EmptyPage:
        prods=allProds.page(allProds.num_pages)
    return render(request,"Ecom/search.html",{"searchProducts":prods,"categories":cats,"cartItems":cartItems,"searchedQuery":query})

def myOrders(request):
    # for cart update
    if request.user.is_authenticated:
            customer=request.user
            order,created=Order.objects.get_or_create(customer=customer,complete=False)
            cartItems=order.get_cart_items
    else:
        cartItems=0

    cats=Categories.objects.all()
    # real code for this function is start from here

    if request.user.is_authenticated:
        orders=Order.objects.filter(customer=request.user)
        # orderList=[order["Order"] for order in orders]
        itemList=[]
        for order in orders:
            items=OrderItem.objects.filter(order=order)
            for item in items:
                itemList.append(item)
        
        # print(itemList)
        itemList.reverse()

        
        return render(request,"Ecom/myOrders.html",{"orders":itemList,"cartItems":cartItems,"categories":cats})
    
    return render(request,"Ecom/myOrders.html",{"orders":[],"cartItems":cartItems,"categories":cats})

def trackOrder(request,order):
    # print(order)
    thatOrder=OrderItem.objects.filter(order=order).first()
    updates=OrderUpdates.objects.filter(ordered_item=thatOrder)
    print(updates)
    allUpdates=[]
    for update in updates:
        allUpdates.append([update.description,update.timeStamp])
    
    allUpdates.reverse()
    print(allUpdates)
    
    if request.user.is_authenticated:
        customer=request.user
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        cartItems=order.get_cart_items
    else:
        cartItems=0

    cats=Categories.objects.all()

    return render(request,"Ecom/tracking.html",{"updates":allUpdates,"cartItems":cartItems,"categories":cats})


def take_input(request):
    if request.method=="POST" and request.POST["action"]=="take_input":
        fname=voice.data_to_enter("First Name")
        lname=voice.data_to_enter("Last Name")
        address=voice.data_to_enter("Address")
        city=voice.data_to_enter("City")
        pincode=voice.data_to_enter("Pin Code")
        pincode.replace(" ", "")
        state=voice.data_to_enter("State")
        phone=voice.data_to_enter("Mobile Number")
        phone.replace(" ","")
        print(fname,lname,address,city,pincode,state,phone)
        param={"fname":fname,"lname":lname,"address":address,"city":city,"pincode":pincode,"state":state,"phone":phone}
        return JsonResponse(param)

    

    
      

