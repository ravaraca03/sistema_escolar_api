from rest_framework import serializers
from rest_framework.authtoken.models import Token
from sistema_escolar_api.models import *
import json

class JSONSerializerField(serializers.Field):

    def to_internal_value(self, data):
        if isinstance(data, list):
            return json.dumps(data)
        elif isinstance(data, str):
            try:
                json.loads(data)
                return data
            except json.JSONDecodeError:
                raise serializers.ValidationError
        return data

    def to_representation(self, value):
        if value is None:
            return []
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return []
        return value

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email')

class AdminSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Administradores
        fields = '__all__'

class AlumnoSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Alumnos
        fields = "__all__"

class MaestroSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Maestros
        fields = '__all__'

class EventosSerializer(serializers.ModelSerializer):
    publico_objetivo = JSONSerializerField()

    class Meta:
        model = Eventos
        fields = '__all__'