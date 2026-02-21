from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from customer import models
from customer.models import (
    Contact,
    Category,
    SubCategory,
    Product,
    customerOrder,
    updateStatus,
    userreview,
    cacnceledorder,
)
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import razorpay
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from . import process, analysis_logic
import math
from django.contrib.auth.models import User
import random
from django.core.mail import send_mail


cat = Category.objects.all()
subcat = SubCategory.objects.all()
context = {"cat": cat, "subcat": subcat}
otp_store = {}
# Create your views here.


def base(request):
    return render(request, "customer/base.html", context)


def index(request):
    product = Product.objects.all()
    context.update({"product": product})
    return render(request, "customer/index.html", context)


def About(request):
    return render(request, "customer/aboutUs.html", context)


def contact(request):
    if request.method == "POST":
        name = request.POST["customerName"]
        email = request.POST["customerEmail"]
        sub = request.POST["contactSubject"]
        desc = request.POST["contactMessage"]
        contact = Contact(name=name, email=email, sub=sub, desc=desc)
        contact.save()
        messages.success(request, "Your Response Has been saved!")
    return render(request, "customer/contactUs.html", context)


def analysis(request):
    total = analysis_logic.totalRevenue()
    totalUsers = User.objects.count()
    totalOrders = customerOrder.objects.count()
    pending = analysis_logic.pendingOrders()
    canceledOrder = analysis_logic.cancelledOrders()
    context.update(
        {
            "total": total,
            "users": totalUsers,
            "orders": totalOrders,
            "orderspermonth": math.ceil(totalOrders / 12),
            "pendingOrders": pending,
            "canceledOrder": canceledOrder,
            "products": Product.objects.count(),
        }
    )
    return render(request, "customer/analysis.html", context)


def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        name = request.POST["name"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        # ✅ Password validation
        try:
            validate_password(pass1)
        except ValidationError as e:
            for error in e:
                messages.error(request, error)
            return redirect("register")

        # ✅ Create user
        myuser = User.objects.create_user(
            username=username, email=email, password=pass1
        )
        myuser.first_name = name
        myuser.save()

        user = authenticate(username=username, password=pass1)
        login(request, user)

        messages.success(request, "Account created successfully!")
        return redirect("index")  # ✅ Change this if your homepage is different

    return render(request, "customer/register.html")


def loginPage(request):
    if request.method == "POST":
        loginusername = request.POST["loginusername"]
        loginpassword = request.POST["loginpassword"]
        # ✅ Password validation
        try:
            validate_password(loginpassword)
        except ValidationError as e:
            for error in e:
                messages.error(request, error)
            return redirect("login")

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In!")
            return redirect(index)
        else:
            messages.error(request, "Invalid Credentials")
    return render(request, "customer/login.html", context)


def logoutPage(request):
    logout(request)
    return redirect("index")


def forgetpassword(request):
    context = {}

    if request.method == "POST":
        action = request.POST.get("action")

        # Step 1: Verify email and send OTP
        if action == "send_otp":
            username = request.POST.get("username")
            email = request.POST.get("email")

            try:
                user = User.objects.get(username=username, email=email)
                otp = random.randint(100000, 999999)
                otp_store[username] = otp  # store OTP temporarily

                send_mail(
                    "Your OTP for Password Reset",
                    f"Hi {username},\n\nYour OTP is {otp}.",
                    "pavankewlani17@gmail.com",
                    [email],
                    fail_silently=False,
                )

                messages.success(request, f"OTP sent to {email}")
                context = {"stage": "otp", "username": username}
            except User.DoesNotExist:
                messages.error(request, "Invalid username or email")

        # Step 2: Verify OTP
        elif action == "verify_otp":
            username = request.POST.get("username")
            entered_otp = request.POST.get("otp")

            real_otp = otp_store.get(username)

            if real_otp and str(real_otp) == entered_otp:
                messages.success(request, "OTP verified")
                context = {"stage": "reset", "username": username}
            else:
                messages.error(request, "Invalid OTP")
                context = {"stage": "otp", "username": username}

        # Step 3: Reset Password
        elif action == "reset_password":
            username = request.POST.get("username")
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")
            try:
                validate_password(new_password)
            except ValidationError as e:
                for error in e:
                    messages.error(request, error)
                return redirect("fpass")

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match")
                context = {"stage": "reset", "username": username}
            else:
                try:
                    user = User.objects.get(username=username)
                    user.set_password(new_password)
                    user.save()
                    otp_store.pop(username, None)  # Clean up
                    messages.success(request, "Password reset successful!")
                    return redirect("login")
                except User.DoesNotExist:
                    messages.error(request, "User not found")
                    context = {"stage": "verify"}

    else:
        context = {"stage": "verify"}

    return render(request, "customer/fpass.html", context)


def shop(request):
    return render(request, "customer/shop.html", context)


def product(request, slug):
    product = Product.objects.filter(name=slug).first()
    review = userreview.objects.filter(product=product)
    context.update({"product": product, "review": review})
    return render(request, "customer/product.html", context)


def wish(request):
    return render(request, "customer/wish.html", context)


def search(request):
    if request.method == "GET":
        search = request.GET["search"]
        if len(search) > 70:
            messages.error(request, "Enter a Valid Keyword to Search")
            product = Product.objects.none()
        else:
            productName = Product.objects.filter(name__icontains=search)
            productContent = Product.objects.filter(srtdesc__icontains=search)
            allProducts = productName.union(productContent)
        if allProducts.count() == 0:
            messages.warning(request, "Search Results not found.")
        context.update({"allProducts": allProducts, "search": search})
    return render(request, "customer/search.html", context)


def addCart(request):
    return render(request, "customer/addCart.html", context)


def checkout(request):
    context.update({"done": False})
    if request.method == "POST":
        email = request.POST["email"]
        productdetails = request.POST["productdetails"]
        totalprice = request.POST["totalprice"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        address = request.POST["address"] + " " + request.POST["address1"]
        city = request.POST["city"]
        state = request.POST["state"]
        pincode = request.POST["pincode"]
        phone = request.POST["phone"]

        if totalprice == 0:
            messages.error(request, "Buy some Products before Checkout.")
            return render(request, "customer/checkout.html", context)

        if (
            len(productdetails) < 1
            or len(firstname) == 0
            or len(lastname) == 0
            or len(address) == 0
            or len(city) == 0
            or len(state) == 0
            or len(pincode) == 0
            or len(phone) > 10
        ):
            messages.error(request, "Fill Appropriate Details to Checkout.")
            return render(request, "customer/checkout.html", context)

        status = process.updateCart(request, productdetails)
        prodDetails = process.prodDetail(productdetails)
        if status:
            order = customerOrder(
                user=request.user,
                email=email,
                productdetails=prodDetails,
                totalprice=totalprice,
                firstname=firstname,
                lastname=lastname,
                address=address,
                city=city,
                state=state,
                pincode=pincode,
                phone=phone,
            )
            order.save()
            messages.success(request, "Order Placed Successfully!")
            process.confirmationMail(email, order.orderId)
            context.update({"done": True})
            request.session["price"] = totalprice
    return render(request, "customer/checkout.html", context)


def payment_process(request):
    key_id = "rzp_test_PvM4GxK9MYlCUc"
    key_secret = "WzsOTRAU4l3oAA1CS7jlVS5E"
    amount = int(request.session["price"]) * 100
    client = razorpay.Client(auth=(key_id, key_secret))
    data = {
        "amount": amount,
        "currency": "INR",
        "receipt": "OIBP",
        "notes": {"name": "AK", "payment_for": "OIBP Test"},
    }
    id = request.user.id
    result = User.objects.get(pk=id)
    payment = client.order.create(data=data)
    context.update({"payment": payment, "result": result})
    return render(request, "customer/payment_process.html", context)


@csrf_exempt
def success(request):
    context = {}
    return render(request, "customer/sucess.html", context)


@csrf_exempt
def Sucess1(request):
    context = {}
    return render(request, "customer/Sucess1.html", context)


def category(request, slug):
    cat = Category.objects.get(name=slug)
    product = Product.objects.filter(category=cat)
    context.update({"product": product})
    return render(request, "customer/category.html", context)


def ordertrack(request, slug=0):
    context.update({"orders": ""})
    if slug == 0:
        if request.method == "POST":
            orderId = request.POST["orderId"]
            orders = customerOrder.objects.filter(orderId=orderId)
            datauser = ""
            for i in orders:
                datauser = i.user
            if datauser == request.user:
                context["orders"] = orders
                print("done")
            # if str(request.user.username) == str(orders.orderId.user):
            #    context.update({"orders": orders})
            # else:
            #    messages.error(request, "Enter valid order ID")

    return render(request, "customer/ordertrack.html", context)


def userorders(request):
    orders = customerOrder.objects.filter(user=request.user)
    context.update({"orders": orders})
    return render(request, "customer/userorders.html", context)


def orderdetails(request, slug):
    orders = customerOrder.objects.get(orderId=slug)
    context.update({"orders": orders})
    return render(request, "customer/orderdetails.html", context)


def filter(request):
    if request.method == "GET":
        category = request.GET["category"]
        price = request.GET["price"]
        if str(category) == "all" and str(price) == "all":
            return redirect("/customer")
        elif str(category) == "all":
            allProduct = Product.objects.filter(price__range=(0, price))
            context.update({"product": allProduct})
        elif str(price) == "all":
            cat_id = Category.objects.get(name=category)
            allProduct = Product.objects.filter(category=cat_id.id)
            context.update({"product": allProduct})
        else:
            cat_id = Category.objects.get(name=category)
            allProduct = Product.objects.filter(
                price__range=(0, price), category=cat_id.id
            )
            context.update({"product": allProduct})
    return render(request, "customer/filter.html", context)


def review(request):
    product = Product.objects.all()
    context.update({"product": product})
    if request.method == "POST":
        productname = request.POST["product"]
        message = request.POST["message"]
        product = Product.objects.get(name=productname)
        rev = userreview(user=request.user, product=product, message=message)
        rev.save()
        messages.success(request, "Review Submitted Successfully")
    return render(request, "customer/review.html", context)


def cancelorder(request, slug=0):
    orders = customerOrder.objects.get(orderId=slug)
    context.update({"orders": orders})
    if slug != 0:
        if request.method == "POST":
            reason = request.POST["reason"]
            res = cacnceledorder(user=request.user, reason=reason)
            res.save()
            order = customerOrder.objects.get(orderId=slug)
            order.delete()
            messages.success(request, "Order Cancelled SuccessFully")
            return redirect(index)
    return render(request, "customer/cancelorder.html", context)
