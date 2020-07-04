from django.urls import path,include
from store.views import *

app_name = "store"

urlpatterns = [
    path("",HomeView.as_view(),name="homepage"),
    path("product/<slug>",ItemView.as_view(),name="product"),
    path("add-to-cart/<slug>",AddToCart.as_view(),name="add-to-cart"),
    path("add-coupon",AddCouponView.as_view(),name="add-coupon"),
    path("remove-from-cart/<slug>",RemoveFromCart.as_view(),name="remove-from-cart"),
    path("remove-item/<slug>",RemoveItem.as_view(),name="remove-item"),
    path("order-summary",OrderSummaryView.as_view(),name="order_summary"),
    path("checkout/",CheckoutView.as_view(),name="checkout")
]