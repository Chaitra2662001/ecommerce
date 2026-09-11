from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

from .forms import RegisterForm, EditProfileForm, ChangePasswordForm
from .models import Product, Profile, Order, OrderItem, Review


# ============================================================
# HOME
# ============================================================

@login_required
def home(request):

    products = Product.objects.all()

    search = request.GET.get("search")
    category = request.GET.get("category")
    sort = request.GET.get("sort")

    if search:
        products = products.filter(name__icontains=search)

    if category:
        products = products.filter(category=category)

    if sort == "price_low":
        products = products.order_by("price")

    elif sort == "price_high":
        products = products.order_by("-price")

    elif sort == "name":
        products = products.order_by("name")

    cart = request.session.get("cart", [])

    cart_count = 0

    for item in cart:

        if isinstance(item, dict):
            cart_count += item.get("quantity", 1)

        else:
            cart_count += 1

    return render(
        request,
        "index.html",
        {
            "products": products,
            "user_name": request.user.username,
            "cart_count": cart_count,
        }
    )


# ============================================================
# PRODUCT DETAIL
# ============================================================

@login_required
def product_detail(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    reviews = Review.objects.filter(
        product=product
    ).order_by("-created_at")

    average_rating = Review.objects.filter(
        product=product
    ).aggregate(
        average=Avg("rating")
    )["average"]

    if average_rating is not None:
        average_rating = round(
            average_rating,
            1
        )

    return render(
        request,
        "product.html",
        {
            "product": product,
            "reviews": reviews,
            "average_rating": average_rating,
        }
    )

@login_required
def add_review(request, id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=id)

        existing_review = Review.objects.filter(
            user=request.user,
            product=product
        ).first()

        if existing_review:
            from django.contrib import messages
            messages.error(
                request,
                "You have already reviewed this product."
            )
            return redirect("product_detail", id=id)

        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        Review.objects.create(
            rating=rating,
            comment=comment,
            user=request.user,
            product=product
        )

        from django.contrib import messages
        messages.success(
            request,
            "Review added successfully!"
        )

    return redirect("product_detail", id=id)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.method == "POST":
        review.rating = request.POST.get("rating")
        review.comment = request.POST.get("comment")
        review.save()

        from django.contrib import messages
        messages.success(
            request,
            "Review updated successfully!"
        )

        return redirect(
            "product_detail",
            id=review.product.id
        )

    return render(
        request,
        "edit_review.html",
        {
            "review": review
        }
    )


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    product_id = review.product.id

    review.delete()

    from django.contrib import messages
    messages.success(
        request,
        "Review deleted successfully!"
    )

    return redirect(
        "product_detail",
        id=product_id
    )

# ============================================================
# REGISTER
# ============================================================

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            if User.objects.filter(
                email=email
            ).exists():

                return render(
                    request,
                    "register.html",
                    {
                        "form": form,
                        "error": "Email already exists."
                    }
                )

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )

            Profile.objects.create(
                user=user,
                name=name
            )

            return redirect("login")

    else:

        form = RegisterForm()

    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )


# ============================================================
# LOGIN
# ============================================================

def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            return redirect("home")

        return render(
            request,
            "login.html",
            {
                "error": "Invalid email or password."
            }
        )

    return render(
        request,
        "login.html"
    )

def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def cancel_order(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)

        if order.status == "Pending":
            order.status = "Cancelled"

            if order.payment_status == "Paid":
                order.payment_status = "Refunded"

            order.save()

    return redirect("orders")


# ============================================================
# PROFILE
# ============================================================

@login_required
def profile(request):

    user = request.user

    profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={
            "name": user.username
        }
    )

    orders = Order.objects.filter(
        user_name=profile.name
    ).order_by("-id")

    reviews = Review.objects.filter(
        user=user
    ).order_by("-created_at")

    profile_user = {
        "name": profile.name,
        "email": user.email
    }

    return render(
        request,
        "profile.html",
        {
            "user": profile_user,
            "orders": orders,
            "reviews": reviews
        }
    )


# ============================================================
# EDIT PROFILE
# ============================================================

@login_required
def edit_profile(request):

    user = request.user

    profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={
            "name": user.username
        }
    )

    if request.method == "POST":

        form = EditProfileForm(
            request.POST
        )

        if form.is_valid():

            profile.name = form.cleaned_data["name"]

            user.email = form.cleaned_data["email"]

            user.save()
            profile.save()

            return redirect("profile")

    else:

        form = EditProfileForm(
            initial={
                "name": profile.name,
                "email": user.email
            }
        )

    return render(
        request,
        "edit_profile.html",
        {
            "form": form
        }
    )


# ============================================================
# CHANGE PASSWORD
# ============================================================

@login_required
def change_password(request):

    if request.method == "POST":

        form = ChangePasswordForm(
            request.POST
        )

        if form.is_valid():

            current_password = form.cleaned_data[
                "current_password"
            ]

            new_password = form.cleaned_data[
                "new_password"
            ]

            confirm_password = form.cleaned_data[
                "confirm_password"
            ]

            if not request.user.check_password(
                current_password
            ):

                return render(
                    request,
                    "change_password.html",
                    {
                        "form": form,
                        "error": "Current password is incorrect."
                    }
                )

            if new_password != confirm_password:

                return render(
                    request,
                    "change_password.html",
                    {
                        "form": form,
                        "error": "New passwords do not match."
                    }
                )

            request.user.set_password(
                new_password
            )

            request.user.save()

            login(
                request,
                request.user
            )

            return redirect("profile")

    else:

        form = ChangePasswordForm()

    return render(
        request,
        "change_password.html",
        {
            "form": form
        }
    )


# ============================================================
# ADD TO CART
# ============================================================

@login_required
def add_to_cart(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    if product.stock <= 0:

        return redirect(
            "product_detail",
            id=id
        )

    quantity = 1
    size = None

    if request.method == "POST":

        try:

            quantity = int(
                request.POST.get(
                    "quantity",
                    1
                )
            )

        except (
            TypeError,
            ValueError
        ):

            quantity = 1

        size = request.POST.get(
            "size"
        )

    if quantity < 1:
        quantity = 1

    if quantity > product.stock:
        quantity = product.stock

    cart = request.session.get(
        "cart",
        []
    )

    cart.append(
        {
            "id": product.id,
            "quantity": quantity,
            "size": size
        }
    )

    request.session["cart"] = cart

    request.session.modified = True

    return redirect("home")


# ============================================================
# INCREASE QUANTITY
# ============================================================

@login_required
def increase_quantity(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    cart = request.session.get(
        "cart",
        []
    )

    for item in cart:

        if (
            isinstance(item, dict)
            and item.get("id") == id
        ):

            current_quantity = item.get(
                "quantity",
                1
            )

            if current_quantity < product.stock:

                item["quantity"] = (
                    current_quantity + 1
                )

            break

        elif item == id:

            cart.remove(item)

            cart.append(
                {
                    "id": id,
                    "quantity": 2,
                    "size": None
                }
            )

            break

    request.session["cart"] = cart

    request.session.modified = True

    return redirect("cart")


# ============================================================
# DECREASE QUANTITY
# ============================================================

@login_required
def decrease_quantity(request, id):

    cart = request.session.get(
        "cart",
        []
    )

    for item in cart:

        if (
            isinstance(item, dict)
            and item.get("id") == id
        ):

            current_quantity = item.get(
                "quantity",
                1
            )

            if current_quantity > 1:

                item["quantity"] = (
                    current_quantity - 1
                )

            else:

                cart.remove(item)

            break

        elif item == id:

            cart.remove(item)

            break

    request.session["cart"] = cart

    request.session.modified = True

    return redirect("cart")


# ============================================================
# REMOVE FROM CART
# ============================================================

@login_required
def remove_from_cart(request, id):

    cart = request.session.get(
        "cart",
        []
    )

    new_cart = []

    for item in cart:

        if isinstance(item, dict):

            if item.get("id") != id:

                new_cart.append(item)

        else:

            if item != id:

                new_cart.append(item)

    request.session["cart"] = new_cart

    request.session.modified = True

    return redirect("cart")


# ============================================================
# CLEAR CART
# ============================================================

@login_required
def clear_cart(request):

    request.session["cart"] = []

    request.session.modified = True

    return redirect("cart")


# ============================================================
# CART
# ============================================================

@login_required
def cart(request):

    cart_items = request.session.get(
        "cart",
        []
    )

    cart_data = []

    total = 0

    for item in cart_items:

        if isinstance(item, dict):

            product_id = item.get("id")

            quantity = item.get(
                "quantity",
                1
            )

            size = item.get(
                "size"
            )

        else:

            product_id = item

            quantity = 1

            size = None

        try:

            product = Product.objects.get(
                id=product_id
            )

        except Product.DoesNotExist:

            continue

        item_total = (
            product.price * quantity
        )

        cart_data.append(
            {
                "product": product,
                "quantity": quantity,
                "size": size,
                "item_total": item_total
            }
        )

        total += item_total

    return render(
        request,
        "cart.html",
        {
            "cart": cart_data,
            "total": total
        }
    )


# ============================================================
# CHECKOUT
# ============================================================

@login_required
def checkout(request):

    cart_items = request.session.get(
        "cart",
        []
    )

    if not cart_items:

        return redirect("cart")

    products = []

    total = 0

    for item in cart_items:

        if isinstance(item, dict):

            product_id = item.get("id")

            quantity = item.get(
                "quantity",
                1
            )

            size = item.get(
                "size"
            )

        else:

            product_id = item

            quantity = 1

            size = None

        try:

            product = Product.objects.get(
                id=product_id
            )

        except Product.DoesNotExist:

            continue

        if product.stock < quantity:

            continue

        products.append(
            {
                "product": product,
                "quantity": quantity,
                "size": size,
                "item_total": (
                    product.price * quantity
                )
            }
        )

        total += (
            product.price * quantity
        )

    if not products:

        return redirect("cart")

    return render(
        request,
        "checkout.html",
        {
            "products": products,
            "total": total,
            "buy_now": False
        }
    )


# ============================================================
# PAYMENT
# ============================================================

@login_required
def payment(request):

    is_buy_now = (
        request.POST.get("buy_now") == "1"
    )

    if is_buy_now:

        cart_items = request.session.get(
            "buy_now",
            []
        )

    else:

        cart_items = request.session.get(
            "cart",
            []
        )

    if not cart_items:

        return redirect("cart")

    products = []

    total = 0

    for item in cart_items:

        if isinstance(item, dict):

            product_id = item.get("id")

            quantity = item.get(
                "quantity",
                1
            )

            size = item.get(
                "size"
            )

        else:

            product_id = item

            quantity = 1

            size = None

        try:

            product = Product.objects.get(
                id=product_id
            )

        except Product.DoesNotExist:

            continue

        if product.stock < quantity:

            continue

        products.append(
            {
                "product": product,
                "quantity": quantity,
                "size": size
            }
        )

        total += (
            product.price * quantity
        )

    if not products:

        return redirect("cart")

    return render(
        request,
        "payment.html",
        {
            "products": products,
            "total": total,
            "buy_now": is_buy_now
        }
    )


# ============================================================
# PROCESS PAYMENT
# ============================================================

@login_required
def process_payment(request):

    if request.method != "POST":

        return redirect("checkout")

    is_buy_now = (
        request.POST.get("buy_now") == "1"
    )

    if is_buy_now:

        cart_items = request.session.get(
            "buy_now",
            []
        )

    else:

        cart_items = request.session.get(
            "cart",
            []
        )

    if not cart_items:

        return redirect("cart")

    products = []

    total = 0

    item_details = []

    # ========================================================
    # CHECK STOCK FIRST
    # ========================================================

    with transaction.atomic():

        for item in cart_items:

            if isinstance(item, dict):

                product_id = item.get("id")

                quantity = item.get(
                    "quantity",
                    1
                )

                size = item.get(
                    "size"
                )

            else:

                product_id = item

                quantity = 1

                size = None

            try:

                product = (
                    Product.objects
                    .select_for_update()
                    .get(id=product_id)
                )

            except Product.DoesNotExist:

                continue

            if product.stock < quantity:

                return redirect("cart")

            products.append(product)

            total += (
                product.price * quantity
            )

            if size:

                item_details.append(
                    f"{product.name} "
                    f"(Size: {size}) "
                    f"x {quantity}"
                )

            else:

                item_details.append(
                    f"{product.name} "
                    f"x {quantity}"
                )

        if not products:

            return redirect("cart")

        # ====================================================
        # REDUCE STOCK
        # ====================================================

        for item in cart_items:

            if isinstance(item, dict):

                product_id = item.get("id")

                quantity = item.get(
                    "quantity",
                    1
                )

            else:

                product_id = item

                quantity = 1

            try:

                product = Product.objects.get(
                    id=product_id
                )

            except Product.DoesNotExist:

                continue

            product.stock -= quantity

            product.save(
                update_fields=["stock"]
            )

        # ====================================================
        # CREATE ORDER
        # ====================================================

        order = Order.objects.create(
            user_name=request.user.username,
            items=", ".join(item_details),
            total=total,
            status="Pending",
            payment_status="Paid"
        )

        # ====================================================
        # CREATE ORDER ITEMS
        # ====================================================

        for item in cart_items:

            if isinstance(item, dict):

                product_id = item.get("id")

                quantity = item.get(
                    "quantity",
                    1
                )

                size = item.get(
                    "size"
                )

            else:

                product_id = item

                quantity = 1

                size = None

            try:

                product = Product.objects.get(
                    id=product_id
                )

            except Product.DoesNotExist:

                continue

            OrderItem.objects.create(
                order=order,
                product_id=product.id,
                product_name=product.name,
                product_price=product.price,
                quantity=quantity,
                size=size or "",
                product_image=product.image
            )

        # ====================================================
        # CLEAR CART
        # ====================================================

        if is_buy_now:

            request.session["buy_now"] = []

        else:

            request.session["cart"] = []

        request.session.modified = True

    return render(
        request,
        "payment_success.html",
        {
            "order": order
        }
    )
# ORDERS
@login_required
def orders(request):
    user_orders = Order.objects.filter(
        user_name=request.user.username
    ).order_by("-id")

    return render(
        request,
        "orders.html",
        {
            "orders": user_orders
        }
    )

@login_required
def wishlist(request):
    wishlist_ids = request.session.get("wishlist", [])

    products = Product.objects.filter(id__in=wishlist_ids)

    return render(
        request,
        "wishlist.html",
        {"products": products}
    )
@login_required
def add_to_wishlist(request, id):
    wishlist_ids = request.session.get("wishlist", [])

    if id not in wishlist_ids:
        wishlist_ids.append(id)

    request.session["wishlist"] = wishlist_ids
    request.session.modified = True

    return redirect("home")