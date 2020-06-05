from django.conf.urls import url

from store.store_app.views import *

urlpatterns = [
    url(r"^login/$", login, name='login'),
    url(r'^login_out/$',login_out,name='login_out'),
    url(r"^register/$",register,name='register'),
    url(r'^index/$',index,name='index'),
    url(r'^management/$',management,name='management'),
    url(r'^manage_member/$',manage_member,name='manage_member'),
    url(r"^login_out/$", login_out),
    url(r"^goods_type/$", goods_type_add),
    url(r"^goods_add/$", goods_add,name='goods_add'),
    url(r"^goods_change/(\d+)/$", goods_change,name='goods_change'),
    url(r"^goods_delete/(\d+)/$", goods_delete),
    url(r"^goods_date/(\d+)/$", goods_date),
    url(r"^goods_list/(\d+)/$", goods_list,name='goods_list'),
    url(r"^member_add/$", member_add,name='member_add'),
    url(r"^member_change/(\d+)/$", member_change),
    url(r"^member_delete/(\d+)/$", member_delete),
    url(r"^personal/$",personal,name='personal'),
    url(r"^personal_change/(\d+)/$",personal_change),
    url(r"^order/(\d+)/$", order),
    url(r"^order_list/(\d+)/$", order_list),
    url(r"^order_delete/(\d+)/$", order_delete),
    url(r"^recent/",recent,name='recent'),
    url(r"^add_money/$", add_money),


]