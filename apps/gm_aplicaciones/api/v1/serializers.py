from rest_framework import serializers
from uuid import UUID

from ...models import Aplicacion

class AplicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aplicacion
        fields = ['id', 'app_name', 'description', 'abbreviation', 'creator_user', 'is_active', 'created']
        read_only_fields = ['id','creator_user', 'created']

    def create(self, validated_data):
        # print(f"ttt {self.context['request']}")
        user = self.context['request'].user
        # Asegúrate de que user.id es un UUID, si es necesario convertirlo:
        if not isinstance(user.id, UUID):
            user_id = UUID(user.id)  # Convierte user.id a UUID si es necesario
        else:
            user_id = user.id

        validated_data['creator_user'] = user_id
        validated_data['is_active'] = True
        return super().create(validated_data)

class ListApplicationForUser(serializers.ModelSerializer):
    class Meta:
        model = Aplicacion
        fields = ['app_name', 'description', 'abbreviation','slug']