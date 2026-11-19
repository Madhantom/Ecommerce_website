from django.contrib import admin
from .models import *



class CatagoryAdmin(admin.ModelAdmin):
    list_display = ('name','image','descripton')
admin.site.register(Catagory,CatagoryAdmin)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Favourite)
