from rest_framework import serializers
from django.db.models.functions import Round
from django.db.models import Avg

from olcha.models import Category,Group,Product,Image,Comment,ProductAttribute


from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.authtoken.models import Token


class UserLoginSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]


class UserRegisterSerializer(serializers.ModelSerializer):
   
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", 
                   "password", "password2"]
        extra_kwargs = {
            'password': {"write_only": True}
        }

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            detail = {
                "detail": "User Already exist!"
            }
            raise ValidationError(detail=detail)
        return username

    def validate(self, instance):
        if instance['password'] != instance['password2']:
            raise ValidationError({"message": "Both password must match"})

        # if User.objects.filter(email=instance['email']).exists():
        #     raise ValidationError({"message": "Email already taken!"})

        return instance

    def create(self, validated_data):
        passowrd = validated_data.pop('password')
        passowrd2 = validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.set_password(passowrd)
        user.save()
        Token.objects.create(user=user)
        return user


class  ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']


class GroupModelSerializer(serializers.ModelSerializer):

    images = ImageModelSerializer(many=True)

    class Meta:
        model = Group
        fields = ['id','group_name','slug','images']
    

class CategoryModelSerializer(serializers.ModelSerializer):
    images = ImageModelSerializer(many=True,read_only=True)
    groups = GroupModelSerializer(many = True,read_only=True)
    class Meta:
        model = Category
        fields = ['id','category_name','slug','images','groups']




class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class CommentModelSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source = 'user.username')
    product_name = serializers.CharField(source='product.product_name')
    class Meta:
        model = Comment
        fields = ['username','message','file','product_name']
        # extra_fields = ['username']
# class  ImageModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Image
#         fields = ['image']

class ProductModelSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.group_name')
    category_name = serializers.CharField(source='group.category.category_name')
    comments = CommentModelSerializer(many = True,read_only=True)
    primary_image = serializers.SerializerMethodField()
    all_images = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    # avg_rating = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()


    # def get_attributes(self,instance):
    #     product_attributes = ProductAttribute.objects.filter(product=instance)
    #     if product_attributes:
    #         attributes = []
    #         for pa in product_attributes:
    #             attributes.append({
    #                 'attribute_id': pa.attribute.id,
    #                 'attribute_name': pa.attribute.attribute_name,
    #                 'attribute_value_id': pa.attribute_value.id,
    #                 'attribute_value': pa.attribute_value.attribute_value
    #             })
    #         return attributes
    #     return None


    def get_attributes(self,instance):
        attributes = ProductAttribute.objects.filter(product=instance).values_list('attribute_id','attribute__attribute_name','attribute_value_id','attribute_value__attribute_value')
        characters = [
            {'attrbute_id':key_id,
            'attribute_name': key_name,
            'attribute_value_id':value_id,
            'attribute_value': value_name

            }
            for key_id,key_name,value_id,value_name in attributes

        ]
        return characters


    def get_is_liked(self,instance):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        all_likes = instance.users_like.all()
        if user in all_likes:
            return True
        else:
            return False


    def get_avg_rating(self,obj):
        avg_rating = Comment.objects.filter(product=obj).aggregate(avg_rating = Round(Avg('rating')))
        if avg_rating.get('avg_rating'):
            return avg_rating.get('avg_rating')
        return 0

    def get_comment_count(self,instance):
        count = Comment.objects.filter(product = instance).count()
        return count

    # def get_avg_rating(self, instance):
    #     comments = Comment.objects.filter(product = instance)
    #     try:
    #         avg_rating = round(sum([comment.rating for comment in comments]))
    #     except ZeroDivisionError:
    #         avg_rating = 0

    #     return avg_rating


    def get_primary_image(self,instance):
        image = Image.objects.filter(product=instance,is_primary=True).first()
        request = self.context.get('request')
        if image:
            image_url = image.image.url
            return request.build_absolute_uri(image_url)
        
        return None

    def get_all_images(self,instance):
        images = Image.objects.filter(product=instance).all()
        request = self.context.get('request')
        all_images = []
        if images:
            for image in images:
                all_images.append(request.build_absolute_uri(image.image.url))

            return all_images




    class Meta:
        model  = Product
        fields = '__all__'
        extra_fields = ['category_name','group_name','primary_image','all_images','comments','is_liked','attributes']



# class UserRegister(serializers.ModelSerializer):
#     password2 = serializers.CharField(style={'input_type':'password'},write_only=True)

#     class Meta:
#         model = User
#         fields = ['username','password','email','password2']

#     def save(self):
#         reg = User(
#             email = self.validated_data['email'],
#             username = self.validate_data['username']

#         )
#         password = self.validate_data['password']
#         password2 = self.validate_data['password2']
#         if password != password2:
#             raise serializers.ValidationError['password':'password does not match']
#         reg.save()
#         return reg 


