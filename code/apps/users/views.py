from django.contrib.auth.hashers import make_password
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from users.models import VerifyCode, UserProfile
from users.serializers import SmsSerializer, UserRegisterSerializer, UserDetailSerializer
from users.utils import send_sms
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler


class SmsViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = SmsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile']
        # 发送短信息 给mobile
        result = send_sms(mobile)  # {}
        if result.get('code') == 200:
            # x向数据库中保存一份
            code = result.get('obj')
            verifyCode = VerifyCode.objects.create(mobile=mobile, code=code)
            if verifyCode:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response({'mobile': '获取的状态码是:%s' % result.get('code'), }, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.authentication import BasicAuthentication, SessionAuthentication


class UserViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = UserProfile.objects.all()

    # serializer_class = UserRegisterSerializer  # UserDetailSerializer

    # 序列化类 是否使用同一个，如果不是同一个则如何变换序列化类
    #  登录验证
    # self.action_map.get('get')
    # self.action_map = {'get':'retrieve','post':'create',....}
    def get_serializer_class(self):
        print('Action:', self.action)
        if self.action == 'retrieve':
            return UserDetailSerializer
        if self.action == 'create':
            return UserRegisterSerializer
        return UserDetailSerializer

    # 用户登录验证
    authentication_classes = (SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication)

    # permission_classes = (IsAuthenticated,)
    # 权限
    def get_permissions(self):
        if self.action == 'retrieve':
            return [IsAuthenticated(), ]
        if self.action == 'create':
            return []
        return []

    #重写get_object  127.0.0.1:8000/users/1/  不依赖1值找用户，而依赖的是header： jwt token
    def get_object(self):
        return self.request.user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        password = make_password(password)
        serializer.validated_data['password'] = password
        user = self.perform_create(serializer)
        # 并登录
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        # 构建一个字典
        dict1 = serializer.data
        dict1['token'] = token
        # dict1['name']=user.name if user.name else user.username
        headers = self.get_success_headers(serializer.data)
        return Response(dict1, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        print('----->', serializer.validated_data)
        user = serializer.save()
        print('========>', user)
        return user
