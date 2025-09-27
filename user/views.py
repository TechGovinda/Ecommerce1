from django.shortcuts import render, redirect
from product.models import *
from .filters import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.decorators import login_required
from django.views import View
from django.urls import reverse


# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "User account has been created sucessfully !"
            )
            return redirect("/register")
        else:
            messages.add_message(
                request, messages.ERROR, "Please provide correct crediential !"
            )
            return render(request, "user/register.html", {"form": form})

    context = {"form": UserCreationForm}
    return render(request, "user/register.html", context)


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data["username"], password=data["password"]
            )
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect("/admins/")

                return redirect("/")

            else:
                messages.add_message(
                    request, messages.ERROR, "Username or Password is invalid"
                )
                return render(request, "user/login.html", {"form": form})
    context = {"form": LoginForm}
    return render(request, "user/login.html", context)


def logout_user(request):
    logout(request)
    return redirect("/login")


def homepage(request):
    user = request.user.id

    product = Product.objects.all().order_by("-id")[:4]
    cart = Cart.objects.filter(user=user)
    data = {"product": product, "items": cart}
    return render(request, "user/homepage.html", data)


def productpage(request):
    user = request.user.id
    product = Product.objects.all().order_by("-id")
    cart = Cart.objects.filter(user=user)
    product_filter = ProductFilter(request.GET, queryset=product)
    product_final = product_filter.qs

    data = {"product": product_final, "product_filter": product_filter, "items": cart}
    return render(request, "user/productpage.html", data)


def aboutus(request):
    return render(request, "user/aboutus.html")


from django.contrib import messages  # import model


@login_required
def contactus(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # ✅ Save contact form data to database
        Contact.objects.create(name=name, email=email, message=message)

        messages.success(
            request, "Thank you for contacting us! Your message has been saved."
        )
        return redirect("contactus")  # reload contact page

    return render(request, "user/contactus.html")


def productdetail(request, product_id):
    user = request.user.id
    product = Product.objects.get(id=product_id)

    cart = Cart.objects.filter(user=user)

    data = {"product": product, "items": cart}
    return render(request, "user/productdetail.html", data)


@login_required
def add_to_cart(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)

    check_items = Cart.objects.filter(user=user, product=product)

    if check_items:
        messages.add_message(
            request, messages.ERROR, "Product is already added in cart"
        )
        return redirect("/productpage")

    else:
        Cart.objects.create(user=user, product=product)
        messages.add_message(
            request, messages.SUCCESS, "Added product successfully in cart"
        )
        return redirect("/cartlist")


@login_required
def cartlist(request):
    user = request.user
    items = Cart.objects.filter(user=user)
    data = {"items": items}
    return render(request, "user/cart.html", data)


@login_required
def order_item(request, product_id, cart_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(id=cart_id)

    if request.method == "POST":
        form = OrderForm(request.POST)
        quantity = request.POST.get("quantity")
        price = product.price
        total_price = int(quantity) * int(price)
        contact_no = request.POST.get("contact_no")
        address = request.POST.get("address")
        email = request.POST.get("email")
        payment_method = request.POST.get("payment_method")

        order = Order.objects.create(
            user=user,
            product=product,
            quantity=quantity,
            total_price=total_price,
            contact_no=contact_no,
            address=address,
            email=email,
            payment_method=payment_method,
        )

        if order.payment_method == "Cash on Delevery":
            cart.delete()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Order has been successfully. Be ready with cash",
            )
            return redirect("/cartlist")
        elif order.payment_method == "Esewa":
            return redirect(
                reverse("esewaform")
                + "?o_id="
                + str(order.id)
                + "&c_id="
                + str(cart.id)
            )
        elif order.payment_method == "Khalti":
            pass
        else:
            messages.add_message(request, messages.ERROR, "invalid payment options ")
            return redirect("/cartlist")

    form = {"form": OrderForm}

    return render(request, "user/orderform.html", form)


def orderlist(request):
    user = request.user
    order = Order.objects.filter(user=user)
    cart = Cart.objects.filter(user=user)
    data = {"order": order, "items": cart}

    return render(request, "user/myorder.html", data)


import uuid
import hmac
import hashlib
import base64
from django.views import View
from django.shortcuts import render, get_object_or_404


class EsewaView(View):
    def get(self, request, *args, **kwargs):
        o_id = request.GET.get("o_id")
        c_id = request.GET.get("c_id")
        cart = get_object_or_404(Cart, id=c_id)
        order = get_object_or_404(Order, id=o_id)

        # generate unique transaction id
        uuid_val = str(uuid.uuid4())

        # helper for HMAC-SHA256
        def genSha256(key, message):
            key = key.encode("utf-8")
            message = message.encode("utf-8")
            hmac_sha256 = hmac.new(key, message, hashlib.sha256)
            return base64.b64encode(hmac_sha256.digest()).decode("utf-8")

        secret_key = "8gBm/:&EnhH.1/q"

        # convert to plain int strings (avoid 100.00 vs 100 mismatch)

        tax_amount = "0"
        service_charge = "0"
        delivery_charge = "0"
        quantity = order.quantity
        amount = str(int(float(order.product.price)) * quantity)

        # total_amount must equal sum of all
        total_amount = str(
            int(amount) + int(tax_amount) + int(service_charge) + int(delivery_charge)
        )

        # prepare signed string in the same order as signed_field_names
        data_to_sign = f"total_amount={total_amount},transaction_uuid={uuid_val},product_code=EPAYTEST"

        signature = genSha256(secret_key, data_to_sign)

        data = {
            "amount": amount,
            "tax_amount": tax_amount,
            "total_amount": total_amount,
            "transaction_uuid": uuid_val,
            "product_code": "EPAYTEST",
            "product_service_charge": service_charge,
            "product_delivery_charge": delivery_charge,
            "success_url": "http://127.0.0.1:8000/esewa/success/",
            "failure_url": "http://127.0.0.1:8000/esewa/failure/",
            "signed_field_names": "total_amount,transaction_uuid,product_code",
            "signature": signature,
        }

        # # 🔍 Debug print to verify
        # print("=== eSewa Payment Debug ===")
        # for k, v in data.items():
        #     print(f"{k}: {v}")
        # print("signed_string:", data_to_sign)
        # print("============================")

        context = {"order": order, "data": data, "cart": cart}
        return render(request, "user/esewa_payment.html", context)


import json


@login_required
def esewa_verify(request, order_id, cart_id):
    if request.method == "GET":
        data = request.GET.get("data")
        decoded_data = base64.b64decode(data).decode("utf-8")
        map_data = json.loads(decoded_data)
        order = Order.objects.get(id=order_id)
        cart = Cart.objects.get(id=cart_id)

        if map_data.get("status") == "COMPLETE":
            order.payment_status = "Completed"
            order.save()
            cart.delete()
            messages.add_message(request, messages.SUCCESS, "Payment Successfull")
            return redirect("/myorder")
        else:
            messages.add_message(request, messages.ERROR, "failed to make a payment")
            return redirect("/myorder")


@login_required
def user_profile(request):
    user = request.user
    data = {"user": user}
    return render(request, "user/profile.html", data)
