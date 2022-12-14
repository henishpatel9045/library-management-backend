from library.utils import is_librarian
from rest_framework import serializers

from custom_auth.models import *


class SignUpSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField(default=None)
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=50)
    confirm_password = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    
    sign_up_as = serializers.ChoiceField(choices=['Member', 'Librarian'])
    
    phone_number = serializers.CharField(max_length=20, required=False)
    address = serializers.CharField(max_length=200, required=False)
    pin_code = serializers.CharField(max_length=10, required=False)
    aadhaar_card_id = serializers.CharField(max_length=20, required=False)
    date_of_birth = serializers.DateField(required=False)
        
    def validate(self, attrs):
        flag = attrs.get('password') == attrs.get('confirm_password')
        if not flag:
            raise serializers.ValidationError("Password and Confirm Password must be same.")
        return super().validate(attrs)
        
    def create(self, validated_data):
        choice = validated_data.get('sign_up_as')
        with transaction.atomic():
            user = UserSerializer(data=validated_data)
            user.is_valid(raise_exception=True)
            validated_data['user'] = user.create(validated_data).pk
            if choice == 'Member':
                member = MemberSerializer(data=validated_data)
                member.is_valid(raise_exception=True)
                validated_data['id'] = member.create(validated_data).user.pk
            else:
                librarien = LibrarianSerializer(data=validated_data)
                librarien.is_valid(raise_exception=True)
                validated_data['id'] = librarien.create(validated_data).user.pk
            return validated_data
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
    
    def update(self, instance, validated_data):
        user = User.objects.update(username=validated_data.get("username", instance.username), 
                                   password=validated_data.get("password", instance.password),
                                   email=validated_data.get("email", instance.email),
                                   first_name=validated_data.get("first_name", instance.first_name),
                                   last_name=validated_data.get("last_name", instance.last_name))
        return user 
    
    def create(self, validated_data):
        validated_data = {'username': validated_data.get('username'), 'email': validated_data.get('email'), 'password': validated_data.get('password'), 'first_name': validated_data.get('first_name'), 'last_name': validated_data.get('last_name')}
        return User.objects.create_user(**validated_data)


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'user', 'phone_number', 'address', 'pin_code', 'aadhaar_card_id', 'date_of_birth')
    
    def run_validation(self, data):
        try:
            if not is_librarian(self.context.user):
                self.get_fields().get("user").queryset = User.objects.filter(pk=self.context.user.pk)
        except AttributeError as e:
            pass
        return super().run_validation(data)
    
    def create(self, validated_data):
        validated_data['user'] = User.objects.get(pk=validated_data.get('user'))
        validated_data = {key: validated_data.get(key) for key in ['user', 'phone_number', 'address', 'pin_code', 'aadhaar_card_id', 'date_of_birth']}
        return Member.objects.create(**validated_data)
        
class LibrarianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Librarian
        fields = ('id', 'user', 'phone_number', 'address', 'pin_code')
    
    def create(self, validated_data):
        validated_data['user'] = User.objects.get(pk=validated_data.get("user"))
        validated_data = {key: validated_data.get(key) for key in ['user', 'phone_number', 'address', 'pin_code']} 
        return Librarian.objects.create(**validated_data)       

        