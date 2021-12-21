from django.urls import path
from . import views
urlpatterns=[
    path("",views.Ehome,name="Ehome"),
    path("login/",views.Elogin,name="Elogin"),
    path("logout/",views.Elogout,name="Elogout"),
    path("signup/",views.Esignup,name="Esignup"),
    path("checkUser/",views.checkUser,name="checkUser"),
    path("about/",views.Eabout,name="Eabout"),
    path("contact/",views.Econtact,name="Econtact"),
    path("checkout/",views.Echeckout,name="Echeckout"),
    path("check_out/<int:order_id>/",views.checkout_mic,name="checkout_mic"),
    path("show-category/<str:category>/",views.showCategory,name="showCategory"),
    path("showProduct/<int:prod_id>/",views.showProduct,name="showProduct"),
    path("cart/",views.cart,name="cart"),
    path("update_item/",views.update_item,name="update_item"),
    path("paymentMode/",views.paymentMode,name="paymentMode"),
    path("search/",views.searchQuery,name="searchQuery"),
    path("my-orders/",views.myOrders,name="myOrders"),
    path("take_input/",views.take_input,name="take_input"),
    path("track-order/<int:order>/",views.trackOrder,name="trackOrder"),
    


]