from rest_framework import serializers

from .models import UseManagement


class UseManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UseManagement
        fields = ('id', 'product')

    def create(self, validated_data):
        user = self.context.get('request').user
        use_management = UseManagement.objects.create(
            **validated_data,
            user=user
        )
        return use_management
