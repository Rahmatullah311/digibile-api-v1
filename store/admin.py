from django.contrib import admin
from .models import Store, store_staff

admin.site.register(Store)
admin.site.register(store_staff.StoreStaff)