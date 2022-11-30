from django.contrib import admin
from .models import Property, SiteUser, Dislikes, Offer
# Register your models here.

admin.site.register(Property)
admin.site.register(SiteUser)
admin.site.register(Dislikes)
admin.site.register(Offer)
