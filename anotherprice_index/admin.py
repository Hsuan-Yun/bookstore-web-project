from django.contrib import admin
from .models import Member, Product, Images, Author, Publisher, Comment, Order_product, Order_data

admin.site.register(Member)
admin.site.register(Product)
admin.site.register(Images)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Comment)
admin.site.register(Order_product)
admin.site.register(Order_data)


