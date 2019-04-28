from datetime import date
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action

from .serializers import UseManagementSerializer
from .serializers import DashboardSerializer
from .serializers import VoucherSerializer
from .models import Voucher
from .models import UseManagement
from .models import Dashboard


class UseManagementViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args):
        today = date.today()
        user_entries = UseManagement.objects.filter(
            user=request.user
        ).filter(timestamp__contains=today).count()
        if user_entries > 4:
            return Response({'não vai rolar'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = UseManagementSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @action(detail=False, methods=['get'])
    def dashboard(self, request, *args):
        queryset = Dashboard.objects.filter(user=request.user).first()
        if queryset:
            serializer = DashboardSerializer(queryset)
            data = serializer.data
        else:
            data = {
                'accumulated_points': 0,
                'saved_cups': 0,
                'consumed_water': 0,
            }
        return Response(data)

    @action(detail=False, methods=['get', 'post'])
    def vouchers(self, request, *args):
        dashboard = Dashboard.objects.filter(user=request.user).first()
        if request.method == 'POST':
            if dashboard.accumulated_points >= 4:
                voucher = Voucher.objects.create(
                    user=request.user,
                    points=dashboard.accumulated_points
                )
                dashboard.accumulated_points = 0
                dashboard.save()
                data = {
                    'id': voucher.id,
                    'points': voucher.points
                }
                return Response(data)
            else:
                return Response({'não vai rolar'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            vouchers = Voucher.objects.filter(user=request.user)
            serializer = VoucherSerializer(vouchers, many=True)
            return Response(serializer.data)
