from django.urls import path
from . import views
from .feeds import RSSFundraiserMsgUpdateFeed, AtomFundraiserMsgUpdateFeed


app_name = 'fundraiser_app'


urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:category_slug>/', views.fundraiser_category_list, name='fundraiser_category_list'),
    path('<slug:category_slug>/create/', views.create, name='create'),
    path('<slug:category_slug>/<int:msg_id>/<slug:slug>/', views.msg_update, name='msg_update'),
    path('<slug:category_slug>/<int:msg_id>/<slug:slug>/edit_msg_update/', views.edit_msg_update, name='edit_msg_update'),
    path('<slug:category_slug>/<int:msg_id>/<slug:slug>/delete_msg_update/', views.delete_msg_update, name='delete_msg_update'),
    path('<slug:category_slug>/<int:fundr_id>/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.detail, name='detail'),
    path('<slug:category_slug>/<int:fundr_id>/<int:year>/<int:month>/<int:day>/<slug:slug>/edit_fundraiser/', views.edit_fundraiser_detail, name='edit_fundraiser_detail'),
    path('<slug:category_slug>/<int:fundr_id>/<int:year>/<int:month>/<int:day>/<slug:slug>/donate/', views.donate, name='donate'),
    path('<slug:category_slug>/<int:fundr_id>/<slug:slug>/feed/rss2/', RSSFundraiserMsgUpdateFeed(), name='rss2_fundraiser_feed'),
    path('<slug:category_slug>/<int:fundr_id>/<slug:slug>/feed/atom1/', AtomFundraiserMsgUpdateFeed(), name='atom1_fundraiser_feed'),
]
