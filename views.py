import json  
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from shop.form import CustomUserForm
from .models import *
from django.contrib import messages

def home(request):
    products=Product.objects.filter(trending=1)
    return render(request,"shop/index.html",{"products":products})

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pas=request.POST.get('password')
            user=authenticate(request, username=name,password=pas)
            if user is not None:
             login(request,user)
             messages.success(request,"Logged in successfully")
             return redirect("/")
            else:
             messages.error(request,"invalid user name or password")
             return redirect("/login")
        return render(request,"shop/login.html")

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out successfully")
    return redirect("/")

def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registraton Success you can Login Now")
            return redirect('login')
    return render (request,"shop/register.html",{'form':form})

def collections(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request,"shop/collections.html",{"category":catagory})

def collectionsview(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        products=Product.objects.filter(catagory__name=name)
        return render(request,"shop/product/index.html",{"products":products,"catagory":name})
    else:
        messages.warning(request,"no such Catagory found")
        return redirect('Collections')

def product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,"shop/product/product_details.html",{"products":products})
        else:
            messages.error(request,"No Such Catagory Found")
            return redirect('Collections')
    else:
        messages.error(request,"No Such Catagory Found")
        return redirect('Collections')
    
def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,"shop/cart.html",{"cart":cart})
    else:
        return redirect("/")

def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart")

def add_to_cart(request):
    if request.headers.get('X-Requested-with')=='XMLHttpRequest': 
        if request.user.is_authenticated:
         data = json.loads(request.body)
         product_qty = data['product_qty']
         product_id = data['product_id']
         product_status=Product.objects.get(id=product_id) 
         if product_status:
             if Cart.objects.filter(user=request.user.id,product_id=product_id):
                 return JsonResponse({'status':'Product alredy in cart'},status=200)
             else:
                 if product_status.quantity>=product_qty:
                     Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                     return JsonResponse({'status':'Product added to cart'},status=200)
                 else:
                     return JsonResponse({'status':'product stock not available'},status=200)        
        else:
            return JsonResponse({'status':'Login to Add cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)


def fav_page(request):
    if request.headers.get('X-Requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
         data=json.loads(request.body)
         product_id=data['product_id']
         product_status=Product.objects.get(id=product_id)
         if product_status:
             if Favourite.objects.filter(user=request.user.id,product_id=product_id):
                 return JsonResponse({'status':'Product alredy in fav'},status=200)
             else:
                 Favourite.objects.create(user=request.user,product_id=product_id)
                 return JsonResponse({'status':'product add to fav'},status=200)
        else:
            return JsonResponse({'status':'Login to Add Fav'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)

def favviewpage(request):
    if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        return render(request,"shop/fav.html",{"fav":fav})
    else:
        return redirect("/")
    
def remove_fav(request,fid):
    item=Favourite.objects.get(id=fid)
    item.delete()
    return redirect("/favviewpage")
