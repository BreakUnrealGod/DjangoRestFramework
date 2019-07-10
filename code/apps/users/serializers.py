import re
from datetime import datetime, timedelta

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import UserProfile, VerifyCode

REGEX = r'^1[35869]\d{9}$'


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        if UserProfile.objects.filter(mobile=mobile).exists():
            raise serializers.ValidationError('此手机号码已注册')
        if not re.match(REGEX, mobile):
            raise serializers.ValidationError('手机号码格式错误')
        return mobile


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'gender', 'email', 'birthday', 'mobile')
        #exclude = ('password', 'last_login', 'is_superuser', 'first_name', 'last_name', 'is_staff', 'is_active')


# 用户的序列化类
class UserRegisterSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, max_length=4, min_length=4,
                                 error_messages={
                                     'required': '必须输入手机验证码',
                                     'max_length': '必须4位验证码',
                                     'min_length': '必须4位验证码'}, write_only=True)

    # http://127.0.0.1:8000/users?username=15010185644&password=123456&code=2013
    def validate_code(self, code):
        verifyCodes = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-send_time')
        if verifyCodes:
            verifyCode = verifyCodes.first()
            time_cha = datetime.now() - timedelta(minutes=10)
            if time_cha > verifyCode.send_time:
                raise serializers.ValidationError('验证码过期')
            if verifyCode.code != code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('重新发送验证码')
        print('======>', code)
        return code

    username = serializers.CharField(required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=UserProfile.objects.all(), message='用户已存在')])

    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = UserProfile
        fields = ('username', 'password', 'mobile', 'code')

    def validate(self, attrs):  # 全局验证    ['username','password','mobile']
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs
