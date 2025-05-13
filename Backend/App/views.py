
import json
from .serializers import *
from django.db.models import Q
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.hashers import check_password, make_password

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class CheckUsernameView(APIView):
    def post(self, request):
        username = request.data['username']
        exists = Profile.objects.filter(username=username).exists()
        return Response({"massage": exists}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    def post(self, request):
        print(request.data)
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['name'] = serializer.validated_data['username']
            password = make_password(serializer.validated_data['password'])
            serializer.validated_data['password'] = password
            user = serializer.save()

            return Response({
                'message': '用户注册成功',
                'user': ProfileSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        print(request.data)
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            try:
                user = Profile.objects.filter(username=username).first()
                if check_password(password, user.password):
                    file_path = "media/user_info.json"
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(ProfileSerializer(user).data, f, ensure_ascii=False, indent=4)
                    request.session['user_id'] = user.id
                    return Response({
                        'message': '登录成功',
                        'user': ProfileSerializer(user).data
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({'message': '密码错误'}, status=status.HTTP_200_OK)
            except Exception:
                return Response({'message': '用户不存在'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_200_OK)


class SettingPasswordView(APIView):
    def post(self, request):
        print(request.data)
        user = Profile.objects.get(id=request.data['id'])
        print(request.data['oldPassword'])
        if check_password(request.data['oldPassword'], user.password):
            user.password = make_password(request.data['newPassword'])
            print(make_password(request.data['newPassword']))
            user.save()
            return Response({
                'message': '修改成功',
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': '旧密码错误',
            }, status=status.HTTP_401_UNAUTHORIZED)

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by('id')
    serializer_class = RoleSerializer
    pagination_class = CustomPageNumberPagination

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all().order_by('id')
    serializer_class = ProfileSerializer
    pagination_class = CustomPageNumberPagination


    def get_queryset(self):
        queryset = super().get_queryset()
        filter_conditions = Q()
        for field in ['role_id']:
            value = self.request.query_params.get(field)
            if value:
                filter_conditions &= Q(**{f"{field}": value})
        return queryset.filter(filter_conditions)
class CanteenViewSet(viewsets.ModelViewSet):
    queryset = Canteen.objects.all().order_by('id')
    serializer_class = CanteenSerializer
    pagination_class = CustomPageNumberPagination

class WindowViewSet(viewsets.ModelViewSet):
    queryset = Window.objects.all().order_by('id')
    serializer_class = WindowSerializer
    pagination_class = CustomPageNumberPagination


    def get_queryset(self):
        queryset = super().get_queryset()
        filter_conditions = Q()
        for field in ['canteen_id']:
            value = self.request.query_params.get(field)
            if value:
                filter_conditions &= Q(**{f"{field}": value})
        return queryset.filter(filter_conditions)
class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all().order_by('id')
    serializer_class = DishSerializer
    pagination_class = CustomPageNumberPagination


    def get_queryset(self):
        queryset = super().get_queryset()
        filter_conditions = Q()
        for field in ['window_id']:
            value = self.request.query_params.get(field)
            if value:
                filter_conditions &= Q(**{f"{field}": value})
        return queryset.filter(filter_conditions)

class DishLikeViewSet(viewsets.ModelViewSet):
    queryset = DishLike.objects.all().order_by('id')
    serializer_class = DishLikeSerializer
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        queryset = super().get_queryset()
        filter_conditions = Q()
        for field in ['user_id','dish_id']:
            value = self.request.query_params.get(field)
            if value:
                filter_conditions &= Q(**{f"{field}": value})
        return queryset.filter(filter_conditions)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user_id = request.session.get('user_id', None)
        if not user_id:
            return None
        user = Profile.objects.filter(id=user_id).first()
        if user.role:
            queryset = queryset.filter(user__id=user_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class DishFavoriteViewSet(viewsets.ModelViewSet):
    queryset = DishFavorite.objects.all().order_by('id')
    serializer_class = DishFavoriteSerializer
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        queryset = super().get_queryset()
        filter_conditions = Q()
        for field in ['user_id','dish_id']:
            value = self.request.query_params.get(field)
            if value:
                filter_conditions &= Q(**{f"{field}": value})
        return queryset.filter(filter_conditions)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user_id = request.session.get('user_id', None)
        if not user_id:
            return None
        user = Profile.objects.filter(id=user_id).first()
        if user.role:
            queryset = queryset.filter(user__id=user_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class DishCommentFrontendViewSet(viewsets.ModelViewSet):
    queryset = DishComment.objects.all().order_by('id')
    serializer_class = DishCommentSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_conditions = Q()
        for field in ['user_id', 'dish_id']:
            value = self.request.query_params.get(field)
            if value:
                filter_conditions &= Q(**{f"{field}": value})
        return queryset.filter(filter_conditions)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        dish_id = request.GET['dish_id']
        if not dish_id:
            return None
        queryset = queryset.filter(dish__id = dish_id )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DishCommentViewSet(viewsets.ModelViewSet):
    queryset = DishComment.objects.all().order_by('id')
    serializer_class = DishCommentSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_conditions = Q()
        for field in ['user_id','dish_id']:
            value = self.request.query_params.get(field)
            if value:
                filter_conditions &= Q(**{f"{field}": value})
        return queryset.filter(filter_conditions)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user_id = request.session.get('user_id', None)
        if not user_id:
            return None
        user = Profile.objects.filter(id=user_id).first()
        if user.role:
            queryset = queryset.filter(user__id=user_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DishOrderViewSet(viewsets.ModelViewSet):
    queryset = DishOrder.objects.all().order_by('id')
    serializer_class = DishOrderSerializer
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        queryset = super().get_queryset()
        filter_conditions = Q()
        for field in ['user_id','dish_id']:
            value = self.request.query_params.get(field)
            if value:
                filter_conditions &= Q(**{f"{field}": value})
        return queryset.filter(filter_conditions)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user_id = request.session.get('user_id', None)
        if not user_id:
            return None
        user = Profile.objects.filter(id=user_id).first()
        if user.role:
            queryset = queryset.filter(user__id=user_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all().order_by('id')
    serializer_class = AddressSerializer
    pagination_class = CustomPageNumberPagination


    def get_queryset(self):
        queryset = super().get_queryset()
        filter_conditions = Q()
        for field in ['user_id']:
            value = self.request.query_params.get(field)
            if value:
                filter_conditions &= Q(**{f"{field}": value})
        return queryset.filter(filter_conditions)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user_id = request.session.get('user_id', None)
        if not user_id:
            return None
        user = Profile.objects.filter(id=user_id).first()
        if user.role:
            queryset = queryset.filter(user__id=user_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class SwiperPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class SwiperViewSet(viewsets.ModelViewSet):
    queryset = Swiper.objects.all().order_by('id')
    serializer_class = SwiperSerializer
    pagination_class = SwiperPagination



class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all().order_by('id')
    serializer_class = FeedbackSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_conditions = Q()
        for field in ['user_id']:
            value = self.request.query_params.get(field)
            if value:
                filter_conditions &= Q(**{f"{field}": value})
        return queryset.filter(filter_conditions)



def get_queryset(data, table):
    if data:
        q_objects = Q()
        for key, value in data.items():
            q_objects &= Q(**{f'{key}__icontains': value})
        queryset = table.objects.filter(q_objects)
    else:
        queryset = table.objects.all()
    return queryset


class RoleSearchView(GenericAPIView):
    pagination_class = CustomPageNumberPagination
    serializer_class = RoleSerializer
    def post(self, request):
        queryset = get_queryset(request.data,Role)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
class ProfileSearchView(GenericAPIView):
    pagination_class = CustomPageNumberPagination
    serializer_class = ProfileSerializer
    def post(self, request):
        queryset = get_queryset(request.data,Profile)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
class CanteenSearchView(GenericAPIView):
    pagination_class = CustomPageNumberPagination
    serializer_class = CanteenSerializer
    def post(self, request):
        queryset = get_queryset(request.data,Canteen)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
class WindowSearchView(GenericAPIView):
    pagination_class = CustomPageNumberPagination
    serializer_class = WindowSerializer
    def post(self, request):
        queryset = get_queryset(request.data,Window)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
class DishSearchView(GenericAPIView):
    pagination_class = CustomPageNumberPagination
    serializer_class = DishSerializer
    def post(self, request):
        queryset = get_queryset(request.data,Dish)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class DishLikeSearchView(GenericAPIView):
    pagination_class = CustomPageNumberPagination
    serializer_class = DishLikeSerializer
    def post(self, request):
        queryset = get_queryset(request.data,DishLike)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class DishFavoriteSearchView(GenericAPIView):
    pagination_class = CustomPageNumberPagination
    serializer_class = DishFavoriteSerializer
    def post(self, request):
        queryset = get_queryset(request.data,DishFavorite)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class DishCommentSearchView(GenericAPIView):
    pagination_class = CustomPageNumberPagination
    serializer_class = DishCommentSerializer
    def post(self, request):
        queryset = get_queryset(request.data,DishComment)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class DishOrderSearchView(GenericAPIView):
    pagination_class = CustomPageNumberPagination
    serializer_class = DishOrderSerializer
    def post(self, request):
        queryset = get_queryset(request.data,DishOrder)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AddressSearchView(GenericAPIView):
    pagination_class = CustomPageNumberPagination
    serializer_class = AddressSerializer
    def post(self, request):
        queryset = get_queryset(request.data,Address)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class SwiperSearchView(GenericAPIView):
    pagination_class = CustomPageNumberPagination
    serializer_class = SwiperSerializer
    def post(self, request):
        queryset = get_queryset(request.data,Swiper)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class FeedbackSearchView(GenericAPIView):
    pagination_class = CustomPageNumberPagination
    serializer_class = FeedbackSerializer
    def post(self, request):
        queryset = get_queryset(request.data,Feedback)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



from django.db.models import Count, Sum, Avg, Max, Min, StdDev, Variance, F
class Dish_DataAnalysisView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            analysis_result = {
                'dish_window_pie_Data': Dish.objects.values('window').annotate(count=Count('id')).order_by('-count')[:5],
            }
            # 返回 JSON 响应
            return Response(analysis_result, status=status.HTTP_200_OK)
    
        except Exception as e:
            # 处理异常
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 支付宝沙箱视图
from alipay import AliPay
from django.http import JsonResponse
from django.conf import settings
import json

def get_alipay():
    """创建支付宝支付实例"""
    return AliPay(
        appid=settings.ALIPAY_CONFIG["APPID"],
        app_notify_url=settings.ALIPAY_CONFIG["NOTIFY_URL"],
        app_private_key_string=settings.ALIPAY_CONFIG["APP_PRIVATE_KEY"],
        alipay_public_key_string=settings.ALIPAY_CONFIG["ALIPAY_PUBLIC_KEY"],
        sign_type="RSA2",
        debug=True  # True 代表沙箱环境
    )

def alipay_pay(request):
    """生成支付链接"""
    data = json.loads(request.body)
    order_id = data.get("order_id")
    total_amount = data.get("total_amount")

    alipay = get_alipay()
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,
        total_amount=str(total_amount),
        subject="商品支付",
        return_url=settings.ALIPAY_CONFIG["RETURN_URL"],
        notify_url=settings.ALIPAY_CONFIG["NOTIFY_URL"]
    )

    pay_url = f"{settings.ALIPAY_CONFIG['GATEWAY']}?{order_string}"
    return JsonResponse({"pay_url": pay_url})

def alipay_notify(request):
    """支付宝异步通知"""
    alipay = get_alipay()
    data = request.POST.dict()
    sign = data.pop("sign", None)

    success = alipay.verify(data, sign)
    if success:
        # 处理订单状态，例如修改为已支付
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "failed"}, status=400)
