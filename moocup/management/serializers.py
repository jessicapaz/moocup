from rest_framework import serializers

from .models import UseManagement
from .models import Dashboard
from .models import Voucher


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
        dashboard = Dashboard.objects.filter(user=user).first()
        if dashboard:
            dashboard.accumulated_points +=  1
            dashboard.saved_cups += 2
            dashboard.consumed_water += 0.4
            dashboard.save()
        else:
            dashboard = Dashboard.objects.create(
                user=user,
                accumulated_points=1,
                saved_cups=2,
                consumed_water=0.4,
            )
        return use_management


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        exclude = ('user',)

class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = '__all__'
