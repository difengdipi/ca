
import os
from uuid import uuid4
from django.db import models


class Role(models.Model):
    role_name = models.CharField(max_length=255, verbose_name='角色名称', null=True, blank=True, default='')
    description = models.TextField(verbose_name='角色描述', null=True, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', null=True, blank=True)

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = '角色'
        db_table = 'Role'


class Profile(models.Model):
    username = models.CharField(max_length=255, verbose_name='用户名', null=True, blank=True, default='', unique=True)
    password = models.CharField(max_length=255, verbose_name='密码', null=True, blank=True, default='')
    student_id = models.CharField(max_length=255, verbose_name='学号', null=True, blank=True, default='')
    name = models.CharField(max_length=255, verbose_name='姓名', null=True, blank=True, default='')
    gender = models.CharField(max_length=255, verbose_name='性别', null=True, blank=True, default='')
    avatar = models.ImageField(upload_to='avatars/', verbose_name='头像', null=True, blank=True, default='avatars/default.png')
    phone = models.CharField(max_length=255, verbose_name='手机号', null=True, blank=True, default='')
    email = models.CharField(max_length=255, verbose_name='邮箱', null=True, blank=True, default='')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, related_name='profiles', verbose_name='角色', null=True, blank=True, default=2)
    dept = models.CharField(max_length=255, verbose_name='所属部门', null=True, blank=True, default='')
    notes = models.TextField(verbose_name='备注', null=True, blank=True, default='')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'
        db_table = 'Profile'


class Canteen(models.Model):
    name = models.CharField(max_length=255, verbose_name='名称', null=True, blank=True, default='')
    description = models.TextField(verbose_name='描述', null=True, blank=True, default='')
    address = models.TextField(verbose_name='地址', null=True, blank=True, default='')
    contact_person = models.CharField(max_length=255, verbose_name='联系人', null=True, blank=True, default='')
    contact_phone = models.CharField(max_length=255, verbose_name='联系电话', null=True, blank=True, default='')
    grade = models.IntegerField(verbose_name='卫生等级', null=True, blank=True, default=0)
    status = models.CharField(max_length=255, verbose_name='营业状态', null=True, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', null=True, blank=True)

    class Meta:
        verbose_name = '食堂'
        verbose_name_plural = '食堂'
        db_table = 'Canteen'


class Window(models.Model):
    canteen = models.ForeignKey(Canteen, on_delete=models.SET_NULL, related_name='canteen_windows', verbose_name='食堂', null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name='名称', null=True, blank=True, default='')
    description = models.TextField(verbose_name='描述', null=True, blank=True, default='')
    business_hours = models.CharField(max_length=255, verbose_name='营业时间', null=True, blank=True, default='')
    contact_person = models.CharField(max_length=255, verbose_name='联系人', null=True, blank=True, default='')
    contact_phone = models.CharField(max_length=255, verbose_name='联系电话', null=True, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', null=True, blank=True)

    class Meta:
        verbose_name = '窗口'
        verbose_name_plural = '窗口'
        db_table = 'Window'


class Dish(models.Model):
    window = models.ForeignKey(Window, on_delete=models.SET_NULL, related_name='window_dishs', verbose_name='窗口', null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name='名称', null=True, blank=True, default='')
    description = models.TextField(verbose_name='地址', null=True, blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格', null=True, blank=True, default=0.00)
    image = models.ImageField(upload_to='images/', verbose_name='图片', null=True, blank=True)
    stock_quantity = models.IntegerField(verbose_name='库存数量', null=True, blank=True, default=0)
    score = models.IntegerField(verbose_name='评分', null=True, blank=True, default=0)
    time = models.DateTimeField(auto_now_add=True, verbose_name='上架时间', null=True, blank=True)

    def like_count(self):
        return self.dishlikes.count()

    def favorite_count(self):
        return self.dishfavorites.count()

    def comment_count(self):
        return self.dishcomments.count()

    def order_count(self):
        return self.dishorders.count()

    class Meta:
        verbose_name = '菜品'
        verbose_name_plural = '菜品'
        db_table = 'Dish'



class DishLike(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='dishlikes', verbose_name='菜品', null=True, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='dishlikes', verbose_name='用户', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间', null=True, blank=True)

    class Meta:
        verbose_name = '点赞'
        verbose_name_plural = '点赞'
        db_table = 'DishLike'



class DishFavorite(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='dishfavorites', verbose_name='菜品', null=True, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='dishfavorites', verbose_name='用户', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间', null=True, blank=True)

    class Meta:
        verbose_name = '收藏'
        verbose_name_plural = '收藏'
        db_table = 'DishFavorite'



class DishOrder(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='dishorders', verbose_name='菜品', null=True, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='dishorders', verbose_name='用户', null=True, blank=True)
    quantity = models.IntegerField(verbose_name='购买数量', null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总价', null=True, blank=True)
    status = models.CharField(max_length=50, verbose_name='订单状态', default='未支付', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='下单时间', null=True, blank=True)

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'
        db_table = 'DishOrder'



class DishComment(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='dishcomments', verbose_name='花卉', null=True, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='dishcomments', verbose_name='用户', null=True, blank=True)
    score = models.IntegerField(verbose_name='评分', null=True, blank=True, default=0)
    content = models.TextField(verbose_name='评论内容', null=True, blank=True)
    image = models.ImageField(upload_to='images/', verbose_name='配图', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评论时间', null=True, blank=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        db_table = 'DishComment'


class Address(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name='user_addresss', verbose_name='用户', null=True, blank=True)
    address = models.TextField(verbose_name='地址', null=True, blank=True, default='')
    phone = models.CharField(max_length=255, verbose_name='联系电话', null=True, blank=True, default='')
    is_default = models.CharField(max_length=255, verbose_name='默认地址', null=True, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', null=True, blank=True)

    class Meta:
        verbose_name = '地址'
        verbose_name_plural = '地址'
        db_table = 'Address'



class Swiper(models.Model):
    title = models.CharField(max_length=255, verbose_name='标题', null=True, blank=True, default='')
    image = models.ImageField(upload_to='swiper/images/', verbose_name='图片', null=True, blank=True)
    location = models.CharField(max_length=255, verbose_name='标题位置', null=True, blank=True, default='')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = '轮播图'
        db_table = 'Swiper'



class Feedback(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name='feedbacks', verbose_name='用户', null=True, blank=True)
    subject = models.CharField(max_length=255, verbose_name='反馈主题', null=True, blank=True, default='')
    message = models.TextField(verbose_name='反馈信息', null=True, blank=True, default='')
    resolved = models.CharField(max_length=255, verbose_name='是否已解决', null=True, blank=True, default='')
    image = models.ImageField(upload_to='feedback/images/', verbose_name='配图', null=True, blank=True)
    video = models.FileField(upload_to='feedback/videos/', verbose_name='视频', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='反馈时间', null=True, blank=True)

    class Meta:
        verbose_name = '系统反馈'
        verbose_name_plural = '系统反馈'
        db_table = 'Feedback'


