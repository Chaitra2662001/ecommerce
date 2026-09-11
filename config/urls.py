"""
URL configuration for config project.
"""


from django.contrib import admin
from django.urls import path, include

from store.views import (
    home,
    product_detail,
    register,
    login_view,
    profile,
    logout_view,
    cancel_order, 
    add_review,
    edit_review,
    delete_review,
    edit_profile,
    change_password,
    add_to_cart,
    increase_quantity,
    decrease_quantity,
    remove_from_cart,
    clear_cart,
    cart,
    checkout,
    payment,
    process_payment,
    orders,
    wishlist,
    add_to_wishlist,
)   

from store.api.views import product_list, product_detail_api

urlpatterns = [

    # ========================================================
    # HOME
    # ========================================================

    path(
        "",
        home,
        name="home",
    ),

    # ========================================================
    # ADMIN
    # ========================================================

    path(
        "admin/",
        admin.site.urls,
    ),

    path("api/products/", product_list, name="api_product_list"),
path("api/products/<int:id>/", product_detail_api, name="api_product_detail"),
    path("api/", include("store.api.urls")),

    # ========================================================
    # PRODUCT
    # ========================================================

    path(
        "product/<int:id>/",
        product_detail,
        name="product_detail",
    ),

    path("add-review/<int:id>/", add_review, name="add_review"),
    path("edit-review/<int:review_id>/", edit_review, name="edit_review"),
    path("delete-review/<int:review_id>/", delete_review, name="delete_review"),
    # ========================================================
    # AUTHENTICATION
    # ========================================================

    path(
        "register/",
        register,
        name="register",
    ),

    path(
        "login/",
        login_view,
        name="login",
    ),

    path(
        "logout/",
        logout_view,
        name="logout",
    ),

    # ========================================================
    # PROFILE
    # ========================================================

    path(
        "profile/",
        profile,
        name="profile",
    ),

    path(
        "edit-profile/",
        edit_profile,
        name="edit_profile",
    ),

    path(
        "change-password/",
        change_password,
        name="change_password",
    ),

    # ========================================================
    # CART
    # ========================================================

    path(
        "add_to_cart/<int:id>",
        add_to_cart,
        name="add_to_cart",
    ),

    path(
        "increase_quantity/<int:id>",
        increase_quantity,
        name="increase_quantity",
    ),

    path(
        "decrease_quantity/<int:id>",
        decrease_quantity,
        name="decrease_quantity",
    ),

    path(
        "remove_from_cart/<int:id>",
        remove_from_cart,
        name="remove_from_cart",
    ),

    path(
        "clear_cart",
        clear_cart,
        name="clear_cart",
    ),

    path(
        "cart",
        cart,
        name="cart",
    ),

    # ========================================================
    # CHECKOUT
    # ========================================================

    path(
        "checkout",
        checkout,
        name="checkout",
    ),

    # ========================================================
    # PAYMENT
    # ========================================================

    path(
        "payment",
        payment,
        name="payment",
    ),

    path(
        "process-payment/",
        process_payment,
        name="process_payment",
    ),

    # ========================================================
    # ORDERS
    # ========================================================

    path(
        "orders",
        orders,
        name="orders",
    ),
    path("cancel-order/<int:order_id>/", cancel_order, name="cancel_order"),
    path("add-to-wishlist/<int:id>/", add_to_wishlist, name="add_to_wishlist"),
    path("wishlist/", wishlist, name="wishlist"),
]