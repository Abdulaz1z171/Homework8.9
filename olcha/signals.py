import os
import json
from django.db.models.signals import post_save,pre_delete
from django.dispatch import receiver
from olcha.models import Category,Product
from django.core.mail import send_mail
from config.settings import BASE_DIR

@receiver(post_save,sender = Category)
def post_save_category(sender,instance,created,**kwargs):
    if created:
        # print(f'New {instance.category_name} created')
        send_mail(
            "Hi bro how are you",
            "Here is the message.",
            "abdulazizaliyev00171@gmail.com",
            ["abdulazizaliyev4542@gmail.com"],
            fail_silently=False,
        )

# def pre_delete_category(sender,instance,**kwargs):
#     print('Category saved json file before deleting')


# pre_delete_category.connect()


@receiver(pre_delete,sender = Category)
def pre_delete_category(sender,instance,**kwargs):
    file_path = os.path.join(BASE_DIR,'olcha/delete_products',f'category_{instance.id}.json')
    category_data = {
        'id': instance.id,
        'category_name': instance.category_name,
        'slug':instance.slug
    }
    with open(file_path,'w') as json_file:
        json.dump(category_data,json_file,indent = 4)
    print('Category saved json file')

    # Signals for product

@receiver(pre_delete,sender = Product)
def pre_delete_product(sender,instance,**kwargs):
    file_path = os.path.join(BASE_DIR,'olcha/delete_products',f'product_{instance.id}.json')
    product_data = {
        'id':instance.id,
        'product_name': instance.product_name,
        # 'description':instance.description,
        # 'price': instance.price,
        # 'quantity' : instance.quantity,
        # 'rating': instance.rating,
        # 'discount': instance.discount,
        # 'group': instance.group,
        # 'users_like': instance.users_like,
        'slug': instance.slug
    }
    with open(file_path,'w') as json_file:
        json.dump(product_data,json_file,indent = 4)
    print('Product saved json file')



@receiver(post_save,sender = Product)
def post_save_category(sender,instance,created,**kwargs):
    if created:
        # print(f'New {instance.category_name} created')
        send_mail(
            "Hi bro how are you ok?",
            "New product created you can see your database",
            "abdulazizaliyev00171@gmail.com",
            ["abdulazizaliyev4542@gmail.com"],
            fail_silently=False,
        )
