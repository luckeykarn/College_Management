from rest_framework import serializers
from ..models import CustomUser
# from deparment.models import Department
# from employee.models import Employee
from accounts.models import CustomUser
# from employee.serializers.employee_serializers import EmployeeListSerializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer #for login
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError



class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        try:
            refresh = RefreshToken(attrs["refresh"])
            user_id = refresh["user_id"]
            user = CustomUser.objects.get(id=user_id)

            access = AccessToken(data['access'])
            access['username'] = user.username
            access['role'] = user.role
            data['access'] = str(access)

            # Include the new refresh token (after rotation)
            if "refresh" in data:
                data['refresh'] = data['refresh']  # pass it back

        except CustomUser.DoesNotExist:
            raise ValidationError({"user": "User not found"})
        except Exception:
            raise ValidationError({"refresh": "Invalid or expired token"})

        return data


class XotusaCustomUserListSerializers(serializers.ModelSerializer):
    # user = EmployeeListSerializers()
    class Meta:
        model = CustomUser
        fields = ['id','email','username','role']
        

class CustomUserListSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id","username","first_name","last_name","email","role","gender","date_joined"]

class CustomUserRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomUserWriteSerializers(serializers.ModelSerializer):
    def validate(self, attrs):
        attrs =  super().validate(attrs)
        attrs['is_active'] = True
        return attrs
    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomTokenObtainPairSerializerAdmin(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # You can add extra custom claims here if you want
        token['username'] = user.username
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.role != "Admin":
            raise serializers.ValidationError(f"You are not authorized to log in Admin login, because you are {self.user.role}")

        # Add extra user info to the response
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'role':self.user.role,
            # Add more fields if needed
            # 'role': self.user.role,  # if using custom user model with role
        }
        return data


class CustomTokenObtainPairSerializerHr(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # You can add extra custom claims here if you want
        token['username'] = user.username
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.role != "HR":
            raise serializers.ValidationError(f"You are not authorized to log in HR login, because you are {self.user.role}")
        # Add extra user info to the response
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'role':self.user.role,
            # Add more fields if needed
            # 'role': self.user.role,  # if using custom user model with role
        }
        return data


class CustomTokenObtainPairSerializerEmployee(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # You can add extra custom claims here if you want
        token['username'] = user.username
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.role != "Employee":
            raise serializers.ValidationError(f"You are not authorized to log in Employee login, because you are {self.user.role}")

        # Add extra user info to the response
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'role':self.user.role,
            # Add more fields if needed
            # 'role': self.user.role,  # if using custom user model with role
        }
        return data

class UserCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    gender = serializers.CharField()


    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            gender=validated_data["gender"],
        )
        user.set_password(validated_data["password"])  # important: hash password!
        user.save()

  
        return user


# from rest_framework.response import Response
# from rest_framework import status

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     tokens = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password', 'first_name', 'last_name', 'tokens']
#         extra_kwargs = {
#             'password': {'write_only': True},
#         }

#     def get_tokens(self, obj):
#         refresh = RefreshToken.for_user(obj)
#         return {
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         }

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = CustomUser(**validated_data)
#         user.set_password(password)
#         user.role = "Employee"  # Default role
#         user.save()
#         return user
