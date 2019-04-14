from datetime import date
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action

from .serializers import UseManagementSerializer
from .models import UseManagement


class UseManagementViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args):
        today = date.today()
        user_entries = UseManagement.objects.filter(
            user=request.user
        ).filter(timestamp__contains=today).count()
        if user_entries > 4:
            return Response({'Não vai rolar'}, status=status.HTTP_406_NOT_ACCEPTABLE)

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
        use = UseManagement.objects.filter(user=request.user).count()
        data = {
            'accumulated_points': use,
            'saved_cups': use * 2,
            'consumed_water': round(0.4 * use, 2)
        }
        return Response(data)
