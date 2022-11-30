
from django.urls import path, include
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index, name="index"),
    path('accounts/logout', views.logout, name="logout"),
    path('logout', TemplateView.as_view(template_name="logout.html"), name="logout_redirect"),
    path('add_property/', views.add_property, name="add_property"),
    path('accounts/login/', views.Login.as_view(), name="login"),
    path('registration/', views.Register.as_view(), name="signup"),
    path('allproperties/', views.all_properties, name="all_properties"),
    path('recommended/', views.recommended_property, name="recommended_property"),
    path('dislike/<int:pid>', views.dislike, name="dislike"),
    path('like/<int:pid>', views.like, name="like"),
    path('property/<int:pid>', views.single_property, name="single_property"),
    path('profile/<str:name>', views.profile, name="profile"),
    path('myproperties/', views.display_own_properties, name="my_properties"),
    path('error/', TemplateView.as_view(template_name="error.html"), name="error"),
    path('editproperty/<int:property_id>', views.edit_property, name='edit_property'),
    path('editpropertypic/<int:property_id>', views.edit_property_picture, name='edit_property_pic'),
    path('edituser/', views.edit_user, name='edit_user'),
    path('edituserpic/', views.edit_user_pic, name='edit_user_pic'),
    path('offers/', views.offers, name='offers'),
    path('accept_offer/<int:oid>', views.accept_offer, name="accept_offer")
]
