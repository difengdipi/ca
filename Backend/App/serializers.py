
from .models import *
from rest_framework import serializers


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RoleSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', allow_null=True, required=False)
    class Meta:
        model = Role
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), source='role', allow_null=True, required=False)
    role = RoleSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'


class CanteenSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', allow_null=True, required=False)
    class Meta:
        model = Canteen
        fields = '__all__'


class WindowSerializer(serializers.ModelSerializer):
    canteen_id = serializers.PrimaryKeyRelatedField(queryset=Canteen.objects.all(), source='canteen', allow_null=True, required=False)
    canteen = CanteenSerializer(read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', allow_null=True, required=False)
    class Meta:
        model = Window
        fields = '__all__'


class DishSerializer(serializers.ModelSerializer):
    window_id = serializers.PrimaryKeyRelatedField(queryset=Window.objects.all(), source='window', allow_null=True, required=False)
    window = WindowSerializer(read_only=True)
    time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', allow_null=True, required=False)
    like_count = serializers.SerializerMethodField()
    favorite_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    order_count = serializers.SerializerMethodField()
    class Meta:
        model = Dish
        fields = '__all__'


    def get_like_count(self, obj):
        return obj.dishlikes.count()

    def get_favorite_count(self, obj):
        return obj.dishfavorites.count()

    def get_comment_count(self, obj):
        return obj.dishcomments.count()

    def get_order_count(self, obj):
        return obj.dishorders.count()

class DishLikeSerializer(serializers.ModelSerializer):
    dish_id = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all(), source='dish', allow_null=True, required=False)
    dish = DishSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), source='user', allow_null=True, required=False)
    user = ProfileSerializer(read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', allow_null=True, required=False)
    
    class Meta:
        model = DishLike
        fields = '__all__'



class DishFavoriteSerializer(serializers.ModelSerializer):
    dish_id = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all(), source='dish', allow_null=True, required=False)
    dish = DishSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), source='user', allow_null=True, required=False)
    user = ProfileSerializer(read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', allow_null=True, required=False)
    
    class Meta:
        model = DishFavorite
        fields = '__all__'



class DishCommentSerializer(serializers.ModelSerializer):
    dish_id = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all(), source='dish', allow_null=True, required=False)
    dish = DishSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), source='user', allow_null=True, required=False)
    user = ProfileSerializer(read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', allow_null=True, required=False)
    
    class Meta:
        model = DishComment
        fields = '__all__'



class DishOrderSerializer(serializers.ModelSerializer):
    dish_id = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all(), source='dish', allow_null=True, required=False)
    dish = DishSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), source='user', allow_null=True, required=False)
    user = ProfileSerializer(read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', allow_null=True, required=False)
    
    class Meta:
        model = DishOrder
        fields = '__all__'



class AddressSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), source='user', allow_null=True, required=False)
    user = ProfileSerializer(read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', allow_null=True, required=False)
    class Meta:
        model = Address
        fields = '__all__'


class SwiperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Swiper
        fields = '__all__'



class FeedbackSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), source='user', allow_null=True, required=False)
    user = ProfileSerializer(read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', allow_null=True, required=False)
    class Meta:
        model = Feedback
        fields = '__all__'


