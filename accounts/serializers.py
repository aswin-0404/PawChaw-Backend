from rest_framework import serializers
from .models  import Register

class Registerserializer(serializers.ModelSerializer):
    confirmpassword=serializers.CharField(write_only=True)
    class Meta:
        model=Register
        fields=['first_name','last_name','phone','email','password','confirmpassword']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def validate_phone(self,value):
        if len(value)<10:
            raise serializers.ValidationError("Phone Number is invalid!")
        return  value
    
    def validate_password(self,value):
        if len(value)<8:
            raise serializers.ValidationError("Password need atleast 8 charector")
        return value
    
    def validate_email(self,value):
        if not value.endswith('.com') or '@' not in value:
            raise serializers.ValidationError("Email format is incorrect")
        return value
    
    def validate(self,data):
        if data['confirmpassword'] != data['password']:
            raise serializers.ValidationError("Password doesn't match")
        return data
    
    def create(self,validated_data):
        validated_data.pop('confirmpassword')
        user=Register.objects.create_user(**validated_data)

        return user
    
class Loginserializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()


