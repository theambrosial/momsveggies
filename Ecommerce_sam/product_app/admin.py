from django.contrib import admin
from .models import Product_model,Category
class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'category', 'selling_cost', 'entry_timedate', )
    list_filter = ('offer','category')

    search_fields = ('name', 'tags')
    ordering = ('id',)
    filter_horizontal = ()

admin.site.register(Product_model,ProductAdmin)
admin.site.register(Category)