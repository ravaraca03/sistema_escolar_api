from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from sistema_escolar_api.serializers import *
from sistema_escolar_api.models import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import mixins


class EventosAll(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EventosSerializer
    queryset = Eventos.objects.all().order_by("id")

class EventosView(mixins.RetrieveModelMixin, generics.CreateAPIView):
    serializer_class = EventosSerializer
    queryset = Eventos.objects.all()

    def get(self, request, *args, **kwargs):
        evento = get_object_or_404(Eventos, id=request.GET.get("id"))
        serializer = self.get_serializer(evento)
        return Response(serializer.data, 200)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        evento = serializer.save()
        return Response({"evento_created_id": evento.id }, status=status.HTTP_201_CREATED)

class EventosViewEdit(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EventosSerializer
    queryset = Eventos.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        evento = get_object_or_404(Eventos, id=request.data.get("id"))
        serializer = self.get_serializer(evento, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        evento = get_object_or_404(Eventos, id=request.GET.get("id"))
        try:
            evento.delete()
            return Response({"details": "Evento eliminado"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error al eliminar evento: {e}")
            return Response({"details": "Error al eliminar"}, status=status.HTTP_400_BAD_REQUEST)

class ResponsablesEventosView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        lista = []

        admins = Administradores.objects.filter(user__is_active=True)
        for admin in admins:
            lista.append({
                "id": f"admin_{admin.id}",
                "nombre": f"{admin.user.first_name} {admin.user.last_name}"
            })

        maestros = Maestros.objects.filter(user__is_active=True)
        for maestro in maestros:
            lista.append({
                "id": f"maestro_{maestro.id}",
                "nombre": f"{maestro.user.first_name} {maestro.user.last_name}"
            })

        return Response(lista, status=200)