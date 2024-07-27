from django.contrib import admin
from olcha.models import  Product,Category,Group,Image,Attribute,AttributeValue,ProductAttribute,Comment

# Register your models here.




admin.site.register(Image)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductAttribute)
admin.site.register(Comment)

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    
    list_display = ['category_name','slug']
    prepopulated_fields = {'slug':('category_name',)}


@admin.register(Group)
class GroupModelAdmin(admin.ModelAdmin):
    
    list_display = ['group_name','slug']
    prepopulated_fields = {'slug':('group_name',)}

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    
    list_display = ['product_name','slug']
    prepopulated_fields = {'slug':('product_name',)}