from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', 'updated_at')

    def create(self, validated_data):
        """Метод для создания объявления."""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)


    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        count_advertisements = Advertisement.objects.filter(status="OPEN", creator=self.context["request"].user).count()
        status = data.get("status")
        if count_advertisements >= 10 and self.context["request"].method == "POST" or status == "OPEN":
            raise serializers.ValidationError("Вы можете создать не более 10 объявлений")
        return data
    
         

    
